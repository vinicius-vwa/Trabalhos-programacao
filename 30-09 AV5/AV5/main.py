import os
from typing import List
from dotenv import load_dotenv
from sqlalchemy import create_engine, String, Integer, Float, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session

load_dotenv()


class Base(DeclarativeBase):
    pass


class Marca(Base):
    __tablename__ = "marcas"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100))
    pais: Mapped[str] = mapped_column(String(100))
    ano: Mapped[int] = mapped_column(Integer())

    modelos: Mapped[List["Modelo"]] = relationship(
        back_populates="marca",
        cascade="all, delete-orphan"
    )


class Modelo(Base):
    __tablename__ = "modelos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100))
    gb: Mapped[int] = mapped_column(Integer())
    preco: Mapped[float] = mapped_column(Float())

    marca_id: Mapped[int] = mapped_column(ForeignKey("marcas.id"))
    marca: Mapped["Marca"] = relationship(back_populates="modelos")


def conectar(tipo):
    if tipo == "1":
        return create_engine("sqlite:///banco_local.db")

    host = os.getenv("MYSQL_HOST")
    user = os.getenv("MYSQL_USER")
    senha = os.getenv("MYSQL_PASSWORD")
    porta = os.getenv("MYSQL_PORT")
    banco = os.getenv("MYSQL_DATABASE")

    return create_engine(
        f"mysql+pymysql://{user}:{senha}@{host}:{porta}/{banco}"
    )


print("\nSistema de Cadastro de Celulares")

print("\nEscolha o banco de dados:")
print("1 - SQLite")
print("2 - MySQL")

tipo = input("Opção: ")

engine = conectar(tipo)
Base.metadata.create_all(engine)

print("\nConexão realizada com sucesso.")

while True:

    print("\nMenu Principal")
    print("1 - Cadastrar Marca")
    print("2 - Cadastrar Modelo")
    print("3 - Listar Registros")
    print("4 - Excluir Modelo")
    print("5 - Excluir Marca")
    print("6 - Trocar Banco")
    print("0 - Sair")

    op = input("\nEscolha uma opção: ")

    with Session(engine) as s:

        if op == "1":

            print("\nCadastro de Marca")

            marca = Marca(
                nome=input("Nome da marca: "),
                pais=input("País de origem: "),
                ano=int(input("Ano de fundação: "))
            )

            s.add(marca)
            s.commit()

            print("\nMarca cadastrada com sucesso!")

        elif op == "2":

            print("\nCadastro de Modelo")

            marcas = s.query(Marca).all()

            if not marcas:
                print("\nNenhuma marca cadastrada.")
                print("Cadastre uma marca primeiro.")
                continue

            print("\nMarcas disponíveis:")

            for m in marcas:
                print(f"{m.id} - {m.nome}")

            modelo = Modelo(
                nome=input("\nNome do modelo: "),
                gb=int(input("Armazenamento (GB): ")),
                preco=float(input("Preço (R$): ")),
                marca_id=int(input("ID da marca: "))
            )

            s.add(modelo)
            s.commit()

            print("\nModelo cadastrado com sucesso!")

        elif op == "3":

            print("\nRegistros Cadastrados")

            marcas = s.query(Marca).all()

            if not marcas:
                print("\nNenhum registro encontrado.")
                continue

            for m in marcas:

                print(f"\nMarca: {m.nome}")
                print(f"País: {m.pais}")
                print(f"Ano de Fundação: {m.ano}")

                if not m.modelos:
                    print("Nenhum modelo cadastrado.")
                else:
                    print("Modelos:")

                    for mod in m.modelos:
                        print(
                            f" - {mod.nome} | "
                            f"{mod.gb}GB | "
                            f"R$ {mod.preco:.2f}"
                        )

        elif op == "4":

            print("\nExcluir Modelo")

            modelo = s.get(
                Modelo,
                int(input("ID do modelo: "))
            )

            if modelo:
                s.delete(modelo)
                s.commit()
                print("\nModelo excluído com sucesso!")
            else:
                print("\nModelo não encontrado.")

        elif op == "5":

            print("\nExcluir Marca")

            marca = s.get(
                Marca,
                int(input("ID da marca: "))
            )

            if marca:
                s.delete(marca)
                s.commit()
                print("\nMarca excluída com sucesso!")
            else:
                print("\nMarca não encontrada.")

        elif op == "6":

            print("\nTrocar Banco de Dados")
            print("1 - SQLite")
            print("2 - MySQL")

            tipo = input("Escolha o banco: ")

            engine = conectar(tipo)
            Base.metadata.create_all(engine)

            print("\nConexão alterada com sucesso.")

        elif op == "0":

            print("\nSistema encerrado.")
            break

        else:
            print("\nOpção inválida.")