from sqlalchemy import Table, Column, ForeignKey

from backend.app.models import Base

from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from backend.app.models import Product

product_catalogue_assoc = Table(
    'product_catalogue_assoc',
    Base.metadata,
    Column('product_id', ForeignKey('table_products.id', ondelete='CASCADE'), primary_key=True),
    Column('catalogue_id', ForeignKey('table_catalogues.id', ondelete='CASCADE'), primary_key=True)
)

class Catalogue(Base):
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    products: Mapped[list["Product"]] = relationship(
        secondary='product_catalogue_assoc',
        back_populates='catalogues'
    )
