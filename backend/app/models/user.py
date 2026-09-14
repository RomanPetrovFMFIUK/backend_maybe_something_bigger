from encodings import unicode_escape
from uuid import uuid4

from backend.app.models import Base

from typing import TYPE_CHECKING

from sqlalchemy.orm import (Mapped,
                            mapped_column,
                            relationship)

if TYPE_CHECKING:
    from backend.app.models import Product


class User(Base):
    name: Mapped[str] = mapped_column(nullable=False)
    products: Mapped[list["Product"]] = relationship(back_populates='user',
                                                     cascade='all, delete-orphan',
                                                     passive_deletes=True)
    password: Mapped[str] = mapped_column(nullable=False, default=lambda: str(uuid4()))
    email: Mapped[str] = mapped_column(unique=True)
    surname: Mapped[str] = mapped_column(nullable=False)
    full_name: Mapped[str] = mapped_column(unique=True)
    age: Mapped[int] = mapped_column(nullable=False)
    admin: Mapped[bool] = mapped_column(nullable=False, default=False, server_default='false')