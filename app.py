import os
from datetime import datetime, timezone

from flask import Flask, request
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base

# 3. Строка подключения собирается из переменных окружения, а не хардкодится
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


# 4. Модель Visit
class Visit(Base):
    __tablename__ = "visits"

    id = Column(Integer, primary_key=True)
    visited_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    ip_address = Column(String(45))


# 5. Создание таблицы при старте приложения
Base.metadata.create_all(bind=engine)

app = Flask(__name__)


# 6. Маршрут GET /hello
@app.route("/hello", methods=["GET"])
def hello():
    session = SessionLocal()
    try:
        visit = Visit(ip_address=request.remote_addr)
        session.add(visit)
        session.commit()
    finally:
        session.close()
    return "Hello", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)