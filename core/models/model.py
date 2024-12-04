from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from .mixins.id_int_pk import IdIntPkMixin

class Model(DeclarativeBase, IdIntPkMixin):
    __abstract__ = True
        