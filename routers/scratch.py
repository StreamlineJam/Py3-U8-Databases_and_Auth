from passlib.context import CryptContext


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

password = "123456"

hashed_password = bcrypt_context.hash(password)

print(hashed_password)

# $2b$12$bDfi7s2eQHG36mTbzafHB.wUTodX53PYe/IxY/dM1A489USNxVpqC
# $2b$12$aFvKfX4TJK86aEjIO5WZIuSCyRT7IRZ1RZa6UqVEJVODrMxm6veTO
