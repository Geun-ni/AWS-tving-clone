"""Pydantic 스키마 - TVING 클론"""
from pydantic import BaseModel
from typing import Optional, List


class UserRegister(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str

class EpisodeResponse(BaseModel):
    id: int
    episode_number: int
    title: Optional[str] = None
    duration: Optional[int] = None
    class Config:
        from_attributes = True

class ContentResponse(BaseModel):
    id: int
    title: str
    category: Optional[str] = None
    genre: Optional[str] = None
    synopsis: Optional[str] = None
    thumbnail_url: Optional[str] = None
    total_seasons: Optional[int] = None
    total_episodes: Optional[int] = None
    episodes: Optional[List[EpisodeResponse]] = None
    class Config:
        from_attributes = True

class WishlistAdd(BaseModel):
    content_id: int

class WatchHistoryAdd(BaseModel):
    content_id: int
    episode_number: int = 1
    watch_position: int = 0

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str
