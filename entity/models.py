from sqlalchemy import String, Integer, DateTime, ForeignKey, Boolean, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime

import pytz

vietnam_timezone = pytz.timezone('Asia/Ho_Chi_Minh')
current_time_in_vietnam = datetime.now(vietnam_timezone)


class BaseModel(DeclarativeBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    created_time: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        default=current_time_in_vietnam
    )
    updated_time: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        default=current_time_in_vietnam,
        onupdate=current_time_in_vietnam
    )


class PairRecord(BaseModel):
    __tablename__ = "pair"
    code: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    signals: Mapped[list["SignalRecord"]] = relationship(
        "SignalRecord",
        back_populates="pair_record",
        cascade="all, delete"
    )

    def __repr__(self):
        return f"PairRecord(id={self.id}, code={self.code})"


class SignalRecord(BaseModel):
    __tablename__ = "signal"
    price: Mapped[float] = mapped_column(Float, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)

    pair_id: Mapped[int] = mapped_column(ForeignKey("pair.id"), nullable=True)
    pair_record: Mapped["PairRecord"] = relationship("PairRecord", back_populates="signals", lazy="joined")

    def __repr__(self):
        return f"SignalRecord(id={self.id}, price={self.price}, user_id={self.user_id})"
