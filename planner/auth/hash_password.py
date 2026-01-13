# 패스워드 암호화 함수
from passlib.context import CryptContext

pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")
# CryptContext: 패스워드 해싱 관리자 클래스
# schemes = ["bcrypt"]: 사용할 해싱 알고리즘
# deprecated="auto": 구버전 알고리즘 자동 처리
#   * 새 알고리즘 나오면 구버전 알아서 권장하지 않게 - 검증은 되지만, 업데이트 안함.

class HashPassword:
    # str을 해싱한 값 반환
    def create_hash(self, password:str):
        return pwd_context.hash(password)
    
    # 평문과 해싱 패스워드 일치 검증
    def verify_hash(self, plain_password: str, hashed_password: str):
        return pwd_context.verify(plain_password, hashed_password)