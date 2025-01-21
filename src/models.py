from src.database import Base
from sqlalchemy import ForeignKey, Enum, JSON, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import DateTime
from typing import Annotated
import enum
from datetime import datetime

intpk = Annotated[int, mapped_column(primary_key=True)]
defstr = Annotated[str, mapped_column(nullable=False)]


class Status(enum.Enum):
    active = "active"
    inactive = "inactive"
    expired = "expired"


class PromoType(enum.Enum):
    common = "COMMON"
    unique = "UNIQUE"


# Companies Table
class CompanyOrm(Base):
    __tablename__ = "companies"

    id: Mapped[intpk]
    title: Mapped[defstr]

    # Relationship with promo codes
    promocodes: Mapped[list["PromocodeOrm"]] = relationship("PromocodeOrm", back_populates="company")


# Promo Codes Table (Base for COMMON and UNIQUE)
class PromocodeOrm(Base):
    __tablename__ = "promocodes"

    id: Mapped[intpk]
    type: Mapped[PromoType]
    title: Mapped[defstr]
    active_from: Mapped[datetime]
    active_until: Mapped[datetime]
    max_count: Mapped[int] = mapped_column(nullable=True)  # For COMMON codes
    targeting: Mapped[dict] = mapped_column(JSON, nullable=True)

    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"))
    company: Mapped["CompanyOrm"] = relationship("CompanyOrm", back_populates="promocodes")

    # Relationships
    unique_codes: Mapped[list["UniquePromocodeOrm"]] = relationship("UniquePromocodeOrm", back_populates="promo")
    likes: Mapped[list["PromoLike"]] = relationship("PromoLike", back_populates="promo")
    comments: Mapped[list["PromoComment"]] = relationship("PromoComment", back_populates="promo")
    activations: Mapped[list["PromoActivation"]] = relationship("PromoActivation", back_populates="promo")


# Unique Promo Codes Table
class UniquePromocodeOrm(Base):
    __tablename__ = "uniquepromocodes"

    id: Mapped[intpk]
    body: Mapped[defstr]
    promo_id: Mapped[int] = mapped_column(ForeignKey("promocodes.id"))

    # Relationship with PromocodeOrm
    promo: Mapped["PromocodeOrm"] = relationship("PromocodeOrm", back_populates="unique_codes")


# Users Table
class UserOrm(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    email: Mapped[defstr] = mapped_column(unique=True)
    password_hash: Mapped[defstr]

    # Relationships
    activations: Mapped[list["PromoActivation"]] = relationship("PromoActivation", back_populates="user")
    likes: Mapped[list["PromoLike"]] = relationship("PromoLike", back_populates="user")
    comments: Mapped[list["PromoComment"]] = relationship("PromoComment", back_populates="user")


# Promo Likes Table
class PromoLike(Base):
    __tablename__ = "promo_likes"

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    promo_id: Mapped[int] = mapped_column(ForeignKey("promocodes.id"))

    # Relationships
    user: Mapped["UserOrm"] = relationship("UserOrm", back_populates="likes")
    promo: Mapped["PromocodeOrm"] = relationship("PromocodeOrm", back_populates="likes")


# Promo Comments Table
class PromoComment(Base):
    __tablename__ = "promo_comments"

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    promo_id: Mapped[int] = mapped_column(ForeignKey("promocodes.id"))
    text: Mapped[defstr]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    # Relationships
    user: Mapped["UserOrm"] = relationship("UserOrm", back_populates="comments")
    promo: Mapped["PromocodeOrm"] = relationship("PromocodeOrm", back_populates="comments")


# Promo Activations Table
class PromoActivation(Base):
    __tablename__ = "promo_activations"

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    promo_id: Mapped[int] = mapped_column(ForeignKey("promocodes.id"))
    activated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    # Relationships
    user: Mapped["UserOrm"] = relationship("UserOrm", back_populates="activations")
    promo: Mapped["PromocodeOrm"] = relationship("PromocodeOrm", back_populates="activations")


# Anti-Fraud Cache Table
class AntifraudCache(Base):
    __tablename__ = "antifraud_cache"

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    promo_id: Mapped[int] = mapped_column(ForeignKey("promocodes.id"))
    status: Mapped[bool]  # Anti-fraud response (True/False)
    cache_until: Mapped[datetime]
