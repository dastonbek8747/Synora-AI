from argon2 import PasswordHasher

ph = PasswordHasher()


def hash_pswd(password: str):
    return ph.hash(password)




def verify_pswd(password: str, hash_password: str) -> bool:
    try:
        return ph.verify(hash_password, password)
    except:
        return False
