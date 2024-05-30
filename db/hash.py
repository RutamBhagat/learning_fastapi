from passlib.context import CryptContext


pwd_ctx = CryptContext(schemes="bcrypt", deprecated="auto")


class Hash:
    def hash_password(self, password):
        return pwd_ctx.hash(password)

    def verify_password(self, password, hashed_password):
        return pwd_ctx.verify(password, hashed_password)
