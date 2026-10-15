import os
from fastapi import FastAPI
from sqladmin import Admin, ModelView
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import Column, Integer, String, Text, Boolean
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL").replace("postgresql+asyncpg://", "postgresql://")

# Базовая модель
class Base(DeclarativeBase):
    pass

# Модель кнопки
class Button(Base):
    __tablename__ = "buttons"
    id = Column(Integer, primary_key=True)
    button_id = Column(String(50), unique=True)
    button_text = Column(String(100))
    button_type = Column(String(20), default="callback")
    parent_menu = Column(String(50), default="main")
    order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)

# Модель ответа
class Answer(Base):
    __tablename__ = "answers"
    id = Column(Integer, primary_key=True)
    button_id = Column(String(50))
    answer_text = Column(Text)
    answer_type = Column(String(20), default="text")
    media_url = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True)

# Создаём приложение
app = FastAPI(title="MAX Bot Admin Panel")

# Подключение к БД (синхронное)
engine = create_engine(DATABASE_URL)
session_maker = sessionmaker(engine, expire_on_commit=False)

# Настройка админ-панели
admin = Admin(app, engine, title="MAX Bot Admin Panel")

# View для кнопок
class ButtonAdmin(ModelView, model=Button):
    column_list = [Button.id, Button.button_id, Button.button_text, Button.parent_menu, Button.order, Button.is_active]
    column_searchable_list = [Button.button_id, Button.button_text]
    column_default_sort = [(Button.order, True)]
    form_columns = [Button.button_id, Button.button_text, Button.button_type, Button.parent_menu, Button.order, Button.is_active]
    name = "Кнопка"
    name_plural = "Кнопки"
    icon = "fa-solid fa-keyboard"

# View для ответов
class AnswerAdmin(ModelView, model=Answer):
    column_list = [Answer.id, Answer.button_id, Answer.answer_text, Answer.answer_type, Answer.is_active]
    column_searchable_list = [Answer.button_id, Answer.answer_text]
    form_columns = [Answer.button_id, Answer.answer_text, Answer.answer_type, Answer.media_url, Answer.is_active]
    name = "Ответ"
    name_plural = "Ответы"
    icon = "fa-solid fa-reply"

# Регистрация View
admin.add_view(ButtonAdmin)
admin.add_view(AnswerAdmin)

@app.get("/")
async def root():
    return {"message": "MAX Bot Admin Panel", "docs": "/docs"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)