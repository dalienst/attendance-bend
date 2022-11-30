from attendance.settings.base import ALLOWED_HOSTS

ALLOWED_HOSTS += [
    "http://localhost:3000",
    "localhost",
    "127.0.0.1",
    "projectattend.netlify.app",
    "attendbend.up.railway.app",
]

DEBUG = True
