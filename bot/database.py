from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
import os
from dotenv import load_dotenv

load_dotenv()

# DATABASE_URL для asyncpg: postgresql+asyncpg://...
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres@localhost/max_bot_db")

# Создаём асинхронный движок
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Функция для получения сессии
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# Функция для получения ответа по button_id
async def get_answer_by_button_id(db: AsyncSession, button_id: str) -> str | None:
    from models import Button, Answer
    
    # Находим кнопку
    stmt = select(Button).where(Button.button_id == button_id, Button.is_active == True)
    result = await db.execute(stmt)
    button = result.scalar_one_or_none()
    
    if not button:
        return None
    
    # Находим активный ответ
    stmt = select(Answer).where(Answer.button_id == button_id, Answer.is_active == True)
    result = await db.execute(stmt)
    answer = result.scalar_one_or_none()
    
    return answer.answer_text if answer else None