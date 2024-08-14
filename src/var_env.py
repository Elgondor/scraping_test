import os

VAR_ENV = {
    'EMAIL': {
        'SENDER': os.getenv("SENDER", 'shokkamax@gmail.com'),
        'USERNAME_SMTP': os.getenv("SENDER", 'shokkamax@gmail.com'),
        'PASSWORD_SMTP': os.getenv("PASSWORD_SMTP", 'oewevzfupalificy'),
        'HOST': os.getenv("HOST", 'smtp.gmail.com'),
        'PORT': os.getenv("PORT", 587),
    },
    'SQLALCHEMY_DATABASE_URI': 'postgresql://baeldung:baeldung@localhost:5432/baeldung',
    'JWT_SECRET_KEY': 'yJhbGciOiJIUzI1NiJ9.eyJSb2xlIjoiQWRtaW4iLCJJc3N1ZXIiOiJJc3N1ZXIiLCJVc2VybmFtZSI6IkphdmFJblVzZSIsImV4cCI6MTcyMzYwNjc1NiwiaWF0IjoxNzIzNjA2NzU2fQ.U6p7sBs75gYBWa5uQGd3mXwKrb91J_qY9N3F0xdnO7Q',
    'FILE_PATH_DATA': 'src/infra/data/',
}

 