# JWT 문자열 인코딩, 디코딩
import time
from datetime import datetime, timezone

from fastapi import HTTPException, status
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError, DecodeError

from database.connection import Settings

settings = Settings()

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_SECONDS = 3600  # 1시간


def create_access_token(user: str) -> str:
    """
    사용자 정보를 담은 JWT access token 생성
    """
    payload = {
        "sub": user,                    # subject (보통 user id 또는 username)
        "iat": time.time(),             # issued at
        "exp": time.time() + ACCESS_TOKEN_EXPIRE_SECONDS,
    }
    
    token = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=ALGORITHM
    )
    return token


def verify_access_token(token: str) -> dict:
    """
    토큰 검증 및 페이로드 반환
    만료되었거나 유효하지 않으면 예외 발생
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"verify_signature": True, "require": ["exp", "iat"]}
        )

        # 추가로 만료 시간 체크 (jwt.decode가 이미 해주지만 명시적으로도 확인 가능)
        expire = payload.get("exp")
        if expire and datetime.now(timezone.utc) > datetime.fromtimestamp(expire, tz=timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token has expired"
            )

        return payload

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token has expired"
        )
    except (InvalidTokenError, DecodeError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Token verification failed: {str(e)}"
        )