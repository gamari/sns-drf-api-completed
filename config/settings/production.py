from .base import *
from decouple import config

# TODO configから読み込むようにする
DEBUG = False
ALLOWED_HOSTS = ["localhost", "0.0.0.0"]
CORS_ORIGIN_WHITELIST=(
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://0.0.0.0:3000"
)