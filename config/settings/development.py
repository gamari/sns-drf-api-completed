from .base import *

print("development")
DEBUG = True
ALLOWED_HOSTS = ["localhost", "0.0.0.0"]
CORS_ORIGIN_WHITELIST=(
    "http://localhost:3000",
)