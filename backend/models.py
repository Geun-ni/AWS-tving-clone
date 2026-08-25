"""SQLAlchemy 모델 - TVING 클론"""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    wishlist = relationship("Wishlist", back_populates="user")
    watch_history = relationship("WatchHistory", back_populates="user")


class Content(Base):
    """콘텐츠 모델 (드라마, 영화, 예능, 다큐)"""
    __tablename__ = "contents"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    category = Column(String(50))  # 드라마, 영화, 예능, 다큐, 애니
    genre = Column(String(100))
    synopsis = Column(Text)
    thumbnail_url = Column(String(500))
    total_seasons = Column(Integer, default=1)
    total_episodes = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    episodes = relationship("Episode", back_populates="content")


class Episode(Base):
    """에피소드 모델"""
    __tablename__ = "episodes"
    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("contents.id"))
    episode_number = Column(Integer, nullable=False)
    title = Column(String(200))
    duration = Column(Integer, default=60)  # 분 단위
    content = relationship("Content", back_populates="episodes")


class Wishlist(Base):
    """찜 목록 모델"""
    __tablename__ = "wishlist"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    content_id = Column(Integer, ForeignKey("contents.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="wishlist")
    content = relationship("Content")


class WatchHistory(Base):
    """시청 이력 모델"""
    __tablename__ = "watch_history"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    content_id = Column(Integer, ForeignKey("contents.id"))
    episode_number = Column(Integer, default=1)
    watch_position = Column(Integer, default=0)  # 초 단위
    progress = Column(Integer, default=0)  # 퍼센트
    watched_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="watch_history")
    content = relationship("Content")
