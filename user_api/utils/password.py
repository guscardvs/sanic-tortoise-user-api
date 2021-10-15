from passlib.context import CryptContext

context = CryptContext(["bcrypt"])


def hash(secret: str) -> str:
    return context.hash(secret)


def validate(password: str, secret: str) -> bool:
    return context.verify(password, secret)
