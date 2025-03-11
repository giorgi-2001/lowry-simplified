import bcrypt


def hash_password(password: str):
    salt = bcrypt.gensalt(10)
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()


def verify_password(hashed: str, password: str):
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed.encode()
    )
