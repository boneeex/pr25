from src.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Annotated
import enum

intpk = Annotated[int, mapped_column(primary_key=True)]
defstr = Annotated[str, mapped_column(nullable=False)]

class CompanyOrm(Base):
    __tablename__ = "companies"

    id: Mapped[intpk]
    title: Mapped[str] = mapped_column(nullable=False)


class UniquePromocodeOrm(Base):
    __tablename__ = "promocodes"

    id: Mapped[intpk]

class UserPromocode(Base):
    id: Mapped[intpk]
    

class UserOrm(Base):
    __tablename__ = "users"
    email: Mapped[defstr]
    password_hash: Mapped[defstr]
