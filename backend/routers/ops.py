"""운영 장애 시뮬레이션 라우터 - CloudWatch 모니터링 및 AI 장애 분석 테스트용"""
import time
import logging
from multiprocessing import Process

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from database import get_db

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/error")
def trigger_error():
    """의도적으로 HTTP 500 오류를 발생시킨다.

    활용:
    - HTTP 5XX 증가
    - CloudWatch Logs ERROR 생성
    - AI 장애 분석
    """
    logger.error("의도적 500 오류 발생 - 장애 시뮬레이션")
    raise RuntimeError("의도적 서버 오류 - 장애 시뮬레이션 테스트")

@router.post("/delay")
def trigger_delay(seconds: int = 5):
    """응답 지연을 발생시킨다.

    활용:
    - TargetResponseTime 증가
    - 응답 지연 분석

    Args:
        seconds: 지연 시간(초). 기본값 5초, 최대 30초.
    """
    delay = min(seconds, 30)  # 최대 30초 제한
    logger.warning(f"의도적 응답 지연 발생: {delay}초")
    time.sleep(delay)
    return {
        "message": "지연 응답 완료",
        "delayed_seconds": delay,
    }

def _cpu_burn(duration: int):
    """CPU를 소모하는 내부 함수"""
    end_time = time.time() + duration
    while time.time() < end_time:
        _ = sum(i * i for i in range(10000))

@router.post("/cpu-load")
def trigger_cpu_load(seconds: int = 10, workers: int = 2):
    """CPU 부하를 발생시킨다.

    활용:
    - CPUUtilization 증가
    - CloudWatch Alarm
    - AI 이상 분석

    Args:
        seconds: 부하 지속 시간(초). 기본값 10초, 최대 60초.
        workers: 병렬 워커 수. 기본값 2, 최대 4.
    """
    duration = min(seconds, 60)
    num_workers = min(workers, 4)

    logger.warning(f"의도적 CPU 부하 발생: {duration}초, 워커 {num_workers}개")

    processes = []
    for _ in range(num_workers):
        p = Process(target=_cpu_burn, args=(duration,))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    return {
        "message": "CPU 부하 시뮬레이션 완료",
        "duration_seconds": duration,
        "workers": num_workers,
    }

@router.post("/db-error")
def trigger_db_error(db: Session = Depends(get_db)):
    """Database 오류를 발생시킨다.

    활용:
    - Database connection timeout
    - RDS 장애 분석
    - Knowledge Base 검색
    """
    logger.error("의도적 DB 오류 발생 - 존재하지 않는 테이블 쿼리")
    try:
        # 존재하지 않는 테이블을 쿼리하여 DB 오류 유발
        db.execute(text("SELECT * FROM non_existent_table_for_chaos_test"))
    except Exception as e:
        logger.error(f"DB 오류 시뮬레이션 성공: {e}")
        raise RuntimeError(f"데이터베이스 오류 시뮬레이션 - {type(e).__name__}: {e}")
