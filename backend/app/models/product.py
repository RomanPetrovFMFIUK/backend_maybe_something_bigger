from backend.app.models import Base

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import (Mapped,
                            mapped_column,
                            relationship)

if TYPE_CHECKING:
    from backend.app.models import User, Catalogue

class Product(Base):
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    amount: Mapped[int] = mapped_column(nullable=False)
    catalogues: Mapped[list["Catalogue"]] = relationship(
        secondary='product_catalogue_assoc',
        back_populates='products'
    )
    user_id: Mapped[str] = mapped_column(ForeignKey('table_users.id', ondelete="CASCADE"))
    user: Mapped["User"] = relationship(back_populates='products')