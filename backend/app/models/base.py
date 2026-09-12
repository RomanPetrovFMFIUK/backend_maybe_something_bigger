from uuid import uuid4

from sqlalchemy.orm import (
    DeclarativeBase,
    declared_attr,
    Mapped,
    mapped_column,
)


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"table_{cls.__name__.lower()}s"

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))