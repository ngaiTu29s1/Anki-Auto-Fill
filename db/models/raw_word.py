import uuid
from enum import Enum as PyEnum
from sqlalchemy import String, Text, DateTime, Enum, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, mapped_column
from db.models.base import Base
# Trạng thái xử lý của từ
class WordStatus(PyEnum):
    QUEUED = "queued"
    ENRICHED = "enriched"
    FLAGGED = "flagged"
    ERROR = "error"

class RawWord(Base):
    __tablename__ = "raw_words"
    __table_args__ = (
        UniqueConstraint("normalized_word", "lang", name="uq_raw_norm_lang"),
    )
    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    word = mapped_column(Text, nullable=False)  # Từ gốc
    normalized_word = mapped_column(Text, nullable=False, index=True)  # Từ chuẩn hóa
    lang = mapped_column(String(8), nullable=False, default="en", index=True)  # Ngôn ngữ
    status = mapped_column(Enum(WordStatus, name="raw_status", native_enum=True),
                          nullable=False, default=WordStatus.QUEUED, index=True)  # Trạng thái
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    note = mapped_column(Text, nullable=True)  # Ghi chú
