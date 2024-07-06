''' Defines the models to be used for the app.
'''
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from . import db


class Base(DeclarativeBase):
    pass


class Product(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    code_name: Mapped[str] = mapped_column(nullable=False)
    in_date: Mapped[int] = mapped_column(nullable=False, unique=True)
    type_of: Mapped[int] = mapped_column(nullable=False)
    is_sold: Mapped[bool] = mapped_column(nullable=False)
    cost: Mapped[float] = mapped_column(nullable=False)
    price: Mapped[float]
    product_code: Mapped[str] = mapped_column(nullable=False, unique=True)


class Console(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    mods: Mapped[str]
    model: Mapped[str] = mapped_column(nullable=False)
    board: Mapped[str] = mapped_column(nullable=False)
    product_code: Mapped[str] = mapped_column(ForeignKey("product.product_code"))
    code_name: Mapped[str] = mapped_column(ForeignKey("product.code_name"))


class Goods(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    product_code: Mapped[str] = mapped_column(ForeignKey("product.product_code"))
    stock: Mapped[int] = mapped_column(nullable=False)
    img_src: Mapped[str] = mapped_column()


class ConsoleType(db.Model):
    code_name: Mapped[str] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(nullable=False)
    img_src: Mapped[str] = mapped_column(nullable=False)
