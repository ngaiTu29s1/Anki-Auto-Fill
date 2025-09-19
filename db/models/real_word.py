import uuid
from enum import Enum as PyEnum
from sqlalchemy import String, Text, DateTime, Enum, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, mapped_column, Mapped
from db.models.base import Base

class RealWord(Base):
    __tablename__ = "real_words"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    word: Mapped[str] = mapped_column(Text, nullable=False)
    phonetic: Mapped[str] = mapped_column(Text, nullable=False)
    english_meaning: Mapped[str] = mapped_column(Text, nullable=False)
    vietnamese_meaning: Mapped[str] = mapped_column(Text, nullable=False)
    example_sentence: Mapped[str] = mapped_column(Text, nullable=False)
    word_audio: Mapped[str | None] = mapped_column(Text, nullable=True)
    image: Mapped[str | None] = mapped_column(Text, nullable=True)
    example_audio: Mapped[str | None] = mapped_column(Text, nullable=True)
    clean_sentence: Mapped[str] = mapped_column(Text, nullable=False)