from uuid import uuid4

from . import Base

from typing import TYPE_CHECKING

from sqlalchemy.orm import (Mapped,
                            mapped_column,
                            relationship)

if TYPE_CHECKING:
    from . import Product


class User(Base):
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    products: Mapped[list["Product"]] = relationship(back_populates='user',
                                                     cascade='all, delete-orphan',
                                                     passive_deletes=True)
    password: Mapped[str] = mapped_column(nullable=False, default=lambda: str(uuid4()))
    email: Mapped[str] = mapped_column(unique=True)