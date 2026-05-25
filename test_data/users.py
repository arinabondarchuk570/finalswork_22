import os
from dataclasses import dataclass

@dataclass
class User:
    email: str
    password: str = os.getenv('BASE_PASSWORD', None)
    name: str = os.getenv('BASE_NAME', None)

CHARLI = User(email='charlie@example.com', password='password123', name='charlie')
ADMIN = User(email='admin@example.com', password='admin123', name='admin')
INVALID_EMAIL_USER = User(email='notcharlie@example.com', password='password123', name='charlie')
INVALID_PASSWORD_USER = User(email='charlie@example.com', password='invalidpassword123', name='charlie')
EMPTY_EMAIL_USER = User(email='', password='password123', name='')
EMPTY_PASSWORD_USER = User(email='charlie@example.com', password='', name='charlie')



