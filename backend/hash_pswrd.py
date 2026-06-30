from argon2 import PasswordHasher

ph = PasswordHasher()


def hash_pswd(password: str):
    return ph.hash(password)


# print(hash_pswd("XUSNURA"))


def verify_pswd(password: str, hash_password: str) -> bool:
    try:
        return ph.verify(hash_password, password)
    except:
        return False

#
# print(verify_pswd("$argon2id$v=19$m=65536,t=3,p=4$gTr9LP3y/9GxbMJ2+5hYTg$oIiZX6nkZ1SUV6+Wy4P/r7jnIv9CX6LQNOYRADfxxNg",
#                   "XUSNURA"))
