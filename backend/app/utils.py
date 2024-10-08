import secrets
import string

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def validate_list(values, class_type):
    return [class_type.model_validate(obj) for obj in values]


async def validate(value, class_type):
    return class_type.model_validate(value)


async def generate_secure_password(length: int = 30):
    characters = string.ascii_letters + string.digits
    password = "".join(secrets.choice(characters) for i in range(length))
    return password
