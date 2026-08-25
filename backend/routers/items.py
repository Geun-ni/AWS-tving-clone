"""콘텐츠/찜/시청기록 라우터 - TVING"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from database import get_db
from schemas import WishlistAdd, WatchHistoryAdd
from crud import (
    get_contents, get_content, get_episodes,
    get_wishlist, add_wishlist, remove_wishlist,
    get_watch_history, add_watch_history
)
from .auth import get_current_user

router = APIRouter()


# ===== 콘텐츠 API =====

@router.get("/contents")
def list_contents(category: Optional[str] = None, limit: int = 50, db: Session = Depends(get_db)):
    """콘텐츠 목록 조회"""
    contents = get_contents(db, category, limit)
    return {"contents": [
        {
            "id": c.id, "title": c.title, "category": c.category,
            "genre": c.genre, "thumbnail_url": c.thumbnail_url,
            "total_seasons": c.total_seasons, "total_episodes": c.total_episodes
        } for c in contents
    ]}


@router.get("/contents/{content_id}")
def get_content_detail(content_id: int, db: Session = Depends(get_db)):
    """콘텐츠 상세 조회 (에피소드 포함)"""
    content = get_content(db, content_id)
    if not content:
        raise HTTPException(status_code=404, detail="콘텐츠를 찾을 수 없습니다.")
    episodes = get_episodes(db, content_id)
    return {
        "id": content.id, "title": content.title,
        "category": content.category, "genre": content.genre,
        "synopsis": content.synopsis, "thumbnail_url": content.thumbnail_url,
        "total_seasons": content.total_seasons, "total_episodes": content.total_episodes,
        "episodes": [
            {"id": ep.id, "episode_number": ep.episode_number, "title": ep.title, "duration": ep.duration}
            for ep in episodes
        ]
    }


# ===== 찜 목록 API =====

@router.get("/wishlist")
def list_wishlist(user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    """찜 목록 조회"""
    items = get_wishlist(db, user_id)
    return [
        {
            "id": item.id,
            "content_id": item.content_id,
            "title": item.content.title,
            "thumbnail_url": item.content.thumbnail_url,
            "genre": item.content.genre
        } for item in items
    ]


@router.post("/wishlist")
def add_to_wishlist(data: WishlistAdd, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    """찜 추가"""
    content = get_content(db, data.content_id)
    if not content:
        raise HTTPException(status_code=404, detail="콘텐츠를 찾을 수 없습니다.")
    add_wishlist(db, user_id, data.content_id)
    return {"message": "찜 목록에 추가되었습니다."}


@router.delete("/wishlist/{content_id}")
def remove_from_wishlist(content_id: int, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    """찜 삭제"""
    success = remove_wishlist(db, user_id, content_id)
    if not success:
        raise HTTPException(status_code=404, detail="찜 목록에 없습니다.")
    return {"message": "찜 목록에서 제거되었습니다."}


# ===== 시청 이력 API =====

@router.get("/history")
def list_history(user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    """시청 이력 조회"""
    items = get_watch_history(db, user_id)
    return [
        {
            "id": item.id,
            "content_id": item.content_id,
            "title": item.content.title,
            "thumbnail_url": item.content.thumbnail_url,
            "episode_number": item.episode_number,
            "progress": item.progress,
            "watched_at": item.watched_at.strftime("%Y-%m-%d %H:%M") if item.watched_at else ""
        } for item in items
    ]


@router.post("/history")
def add_history(data: WatchHistoryAdd, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    """시청 기록 추가/업데이트"""
    content = get_content(db, data.content_id)
    if not content:
        raise HTTPException(status_code=404, detail="콘텐츠를 찾을 수 없습니다.")
    add_watch_history(db, user_id, data.content_id, data.episode_number, data.watch_position)
    return {"message": "시청 기록이 저장되었습니다."}
