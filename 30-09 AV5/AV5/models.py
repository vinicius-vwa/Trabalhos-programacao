from typing import List
from sqlalchemy import String, Float, ForeignKey, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Marca(Base):
    __tablename__ = "tabela_marcas"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(100))
    pais_origem: Mapped[str] = mapped_column(String(100))
    ano_fundacao: Mapped[int] = mapped_column(Integer())

    modelos: Mapped[List["Modelo"]] = relationship(
        back_populates="marca", 
        cascade="all, delete-orphan"
    )

class Modelo(Base):
    __tablename__ = "tabela_modelos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome_modelo: Mapped[str] = mapped_column(String(150))
    armazenamento_gb: Mapped[int] = mapped_column(Integer())
    preco: Mapped[float] = mapped_column(Float())

    marca_id: Mapped[int] = mapped_column(ForeignKey("tabela_marcas.id"))

    marca: Mapped["Marca"] = relationship(back_populates="modelos")
