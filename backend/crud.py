"""CRUD 함수 - TVING 클론"""
from sqlalchemy.orm import Session
import bcrypt
from models import User, Content, Episode, Wishlist, WatchHistory



# ===== 사용자 =====
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, username: str, email: str, password: str):
    user = User(username=username, email=email, hashed_password=bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8"))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))


# ===== 콘텐츠 =====
def get_contents(db: Session, category: str = None, limit: int = 50):
    query = db.query(Content)
    if category:
        query = query.filter(Content.category == category)
    return query.limit(limit).all()

def get_content(db: Session, content_id: int):
    return db.query(Content).filter(Content.id == content_id).first()

def get_episodes(db: Session, content_id: int):
    return db.query(Episode).filter(Episode.content_id == content_id).order_by(Episode.episode_number).all()


# ===== 찜 목록 =====
def get_wishlist(db: Session, user_id: int):
    return db.query(Wishlist).filter(Wishlist.user_id == user_id).all()

def add_wishlist(db: Session, user_id: int, content_id: int):
    existing = db.query(Wishlist).filter(
        Wishlist.user_id == user_id, Wishlist.content_id == content_id
    ).first()
    if existing:
        return existing
    item = Wishlist(user_id=user_id, content_id=content_id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def remove_wishlist(db: Session, user_id: int, content_id: int):
    item = db.query(Wishlist).filter(
        Wishlist.user_id == user_id, Wishlist.content_id == content_id
    ).first()
    if item:
        db.delete(item)
        db.commit()
        return True
    return False


# ===== 시청 이력 =====
def get_watch_history(db: Session, user_id: int):
    return db.query(WatchHistory).filter(
        WatchHistory.user_id == user_id
    ).order_by(WatchHistory.watched_at.desc()).all()

def add_watch_history(db: Session, user_id: int, content_id: int, episode_number: int, watch_position: int = 0):
    # 기존 기록 업데이트 또는 새로 생성
    existing = db.query(WatchHistory).filter(
        WatchHistory.user_id == user_id,
        WatchHistory.content_id == content_id,
        WatchHistory.episode_number == episode_number
    ).first()
    if existing:
        existing.watch_position = watch_position
        existing.progress = min(100, watch_position // 6)  # 간단한 진행률 계산
        db.commit()
        db.refresh(existing)
        return existing
    
    history = WatchHistory(
        user_id=user_id,
        content_id=content_id,
        episode_number=episode_number,
        watch_position=watch_position,
        progress=min(100, watch_position // 6)
    )
    db.add(history)
    db.commit()
    db.refresh(history)
    return history


# ===== 챗봇용 =====
def get_all_contents_for_chat(db: Session):
    return db.query(Content).all()

def get_user_history_for_chat(db: Session, user_id: int):
    return db.query(WatchHistory).filter(WatchHistory.user_id == user_id).all()
