from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

class Sale(Base):
    __tablename__ = 'sale'
    date: Mapped[str] = mapped_column()
    products: Mapped[List["Product"]] = relationship(back_populates="sale", lazy="selectin")

class Product(Base):
    __tablename__ = 'product'
    name: Mapped[str] = mapped_column()
    quantity: Mapped[int] = mapped_column()
    price: Mapped[float] = mapped_column()
    sale_id: Mapped[int] = mapped_column(ForeignKey('sale.id'), default=None, nullable=True)
    sale: Mapped["Sale"] = relationship(back_populates="products")
