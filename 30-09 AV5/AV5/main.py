
import os
from typing import List
from dotenv import load_dotenv
from sqlalchemy import String, Float, ForeignKey, Integer, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# ----------------------------------------------------------------------
# 1. MAPEAMENTO DAS CLASSES (Marca 1 x N Modelo)
# ----------------------------------------------------------------------
class Base(DeclarativeBase):
    pass

class Marca(Base):
    __tablename__ = "tabela_marcas"

    # 4 Atributos
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(100))
    pais_origem: Mapped[str] = mapped_column(String(100))
    ano_fundacao: Mapped[int] = mapped_column(Integer())

    # Relacionamento 1 para N com Modelo
    modelos: Mapped[List["Modelo"]] = relationship(
        back_populates="marca", 
        cascade="all, delete-orphan"
    )

class Modelo(Base):
    __tablename__ = "tabela_modelos"

    # 4 Atributos
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome_modelo: Mapped[str] = mapped_column(String(150))
    armazenamento_gb: Mapped[int] = mapped_column(Integer())
    preco: Mapped[float] = mapped_column(Float())

    # Chave Estrangeira
    marca_id: Mapped[int] = mapped_column(ForeignKey("tabela_marcas.id"))

    # Relacionamento N para 1 com Marca
    marca: Mapped["Marca"] = relationship(back_populates="modelos")


# ----------------------------------------------------------------------
# 2. CONEXÃO COM BANCOS DE DADOS
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# 2. CONEXÃO COM BANCOS DE DADOS
# ----------------------------------------------------------------------
def get_engine(tipo_bd: str):
    if tipo_bd == "sqlite":
        return create_engine("sqlite:///banco_local.db", echo=False)
    elif tipo_bd == "mysql":
        host = os.getenv("MYSQL_HOST")
        user = os.getenv("MYSQL_USER")
        senha = os.getenv("MYSQL_PASSWORD")
        porta = os.getenv("MYSQL_PORT", "12960")
        db = os.getenv("MYSQL_DATABASE", "defaultdb")
        
        url = f"mysql+pymysql://{user}:{senha}@{host}:{porta}/{db}"
        return create_engine(
            url, 
            connect_args={"ssl": {"check_hostname": False}}, 
            echo=False
        )
    else:
        raise ValueError("Tipo de banco inválido")

# CERTIFIQUE-SE DE QUE ESTA FUNÇÃO ESTÁ PRESENTE NO SEU CÓDIGO:
def init_db(engine):
    Base.metadata.create_all(engine)


# ----------------------------------------------------------------------
# 3. INTERFACE DE TERMINAL
# ----------------------------------------------------------------------
def menu_banco():
    while True:
        print("\n=== ESCOLHA O BANCO DE DADOS ===")
        print("1. SQLite (Local)")
        print("2. MySQL (Nuvem / Aiven)")
        op = input("Opção: ").strip()
        if op == "1":
            return "sqlite"
        elif op == "2":
            return "mysql"
        print("Opção inválida! Tente novamente.")

def menu_principal():
    print("\n" + "="*35)
    print("  SISTEMA DE CELULARES (AV5)")
    print("="*35)
    print("1. Inserir Marca")
    print("2. Inserir Modelo de Celular")
    print("3. Listar Marcas e Modelos")
    print("4. Excluir Modelo")
    print("5. Excluir Marca")
    print("6. Alterar Conexão do Banco")
    print("0. Sair")
    print("="*35)

def main():
    tipo_bd = menu_banco()
    engine = get_engine(tipo_bd)
    init_db(engine)
    print(f"\n Conectado ao banco: {tipo_bd.upper()}")

    while True:
        menu_principal()
        op = input("Escolha uma opção: ").strip()

        with Session(engine) as session:
            if op == "1":
                nome = input("Nome da Marca (ex: Apple, Samsung): ")
                pais = input("País de Origem: ")
                ano = int(input("Ano de Fundação: "))
                marca = Marca(nome=nome, pais_origem=pais, ano_fundacao=ano)
                session.add(marca)
                session.commit()
                print(" Marca inserida com sucesso!")

            elif op == "2":
                marcas = session.query(Marca).all()
                if not marcas:
                    print(" Nenhuma marca cadastrada! Cadastre uma marca primeiro.")
                    continue
                
                print("\nMarcas disponíveis:")
                for m in marcas:
                    print(f"ID {m.id} - {m.nome}")
                
                marca_id = int(input("ID da Marca do celular: "))
                nome_modelo = input("Nome do Modelo (ex: Galaxy S24, iPhone 15): ")
                arm = int(input("Armazenamento interno (em GB): "))
                preco = float(input("Preço (R$): "))
                
                modelo = Modelo(
                    nome_modelo=nome_modelo, 
                    armazenamento_gb=arm, 
                    preco=preco, 
                    marca_id=marca_id
                )
                session.add(modelo)
                session.commit()
                print(" Modelo inserido com sucesso!")

            elif op == "3":
                marcas = session.query(Marca).all()
                if not marcas:
                    print(" Nenhum registro encontrado.")
                for m in marcas:
                    print(f"\n[Marca {m.id}] {m.nome} - Origem: {m.pais_origem} ({m.ano_fundacao})")
                    if m.modelos:
                        for mod in m.modelos:
                            print(f"   └── [Modelo {mod.id}] {mod.nome_modelo} | {mod.armazenamento_gb}GB | R$ {mod.preco:.2f}")
                    else:
                        print("   └── Nenhum modelo cadastrado para esta marca.")

            elif op == "4":
                mod_id = int(input("ID do Modelo a excluir: "))
                modelo = session.query(Modelo).filter_by(id=mod_id).first()
                if modelo:
                    session.delete(modelo)
                    session.commit()
                    print(" Modelo excluído com sucesso!")
                else:
                    print(" Modelo não encontrado.")

            elif op == "5":
                marca_id = int(input("ID da Marca a excluir (excluirá também os modelos associados): "))
                marca = session.query(Marca).filter_by(id=marca_id).first()
                if marca:
                    session.delete(marca)
                    session.commit()
                    print(" Marca e seus modelos foram excluídos com sucesso!")
                else:
                    print(" Marca não encontrada.")

            elif op == "6":
                tipo_bd = menu_banco()
                engine = get_engine(tipo_bd)
                init_db(engine)
                print(f"\n Conexão alterada para: {tipo_bd.upper()}")

            elif op == "0":
                print("Saindo do programa...")
                break

if __name__ == "__main__":
    main()
