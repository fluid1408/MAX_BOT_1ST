import asyncio
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, text

# Импорты для maxapi
from maxapi import Bot, Dispatcher, F
from maxapi.filters.command import Command
from maxapi.types import MessageCreated, BotStarted, MessageCallback
from maxapi.types import CallbackButton, LinkButton
from maxapi.utils.inline_keyboard import InlineKeyboardBuilder

load_dotenv()
BOT_TOKEN = os.getenv("MAX_BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./bot.db")

# Модели
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, Text, Boolean

class Base(DeclarativeBase):
    pass

class Button(Base):
    __tablename__ = "buttons"
    id = Column(Integer, primary_key=True)
    button_id = Column(String(50), unique=True)
    button_text = Column(String(100))
    button_type = Column(String(20))
    parent_menu = Column(String(50))
    order = Column(Integer)
    is_active = Column(Boolean, default=True)

class Answer(Base):
    __tablename__ = "answers"
    id = Column(Integer, primary_key=True)
    button_id = Column(String(50))
    answer_text = Column(Text)
    answer_type = Column(String(20))
    media_url = Column(String(500))
    is_active = Column(Boolean, default=True)

# Подключение к БД
engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Создание бота и диспетчера
bot = Bot(BOT_TOKEN)
dp = Dispatcher()

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ База данных инициализирована")

async def seed_db():
    async with AsyncSessionLocal() as db:
        result = await db.execute(text("SELECT COUNT(*) FROM buttons"))
        if result.scalar() > 0:
            return

        if os.path.exists("seed.sql"):
            import sqlite3
            db_path = "/data/bot.db" if os.path.exists("/data") else "./bot.db"
            conn = sqlite3.connect(db_path)
            with open("seed.sql", "r", encoding="utf-8") as f:
                conn.executescript(f.read())
            conn.close()
            print("✅ База данных успешно заполнена через seed.sql!")

async def get_answer(button_id: str):
    async with AsyncSessionLocal() as db:
        stmt = select(Answer).where(Answer.button_id == button_id, Answer.is_active == True)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

async def has_children(button_id: str) -> bool:
    async with AsyncSessionLocal() as db:
        stmt = select(Button).where(Button.parent_menu == button_id, Button.is_active == True)
        result = await db.execute(stmt)
        return result.scalars().first() is not None

async def get_keyboard(parent_id: str):
    """Универсальная функция для построения клавиатуры (главной или подменю)"""
    async with AsyncSessionLocal() as db:
        stmt = select(Button).where(
            Button.is_active == True,
            Button.parent_menu == parent_id
        ).order_by(Button.order)
        result = await db.execute(stmt)
        buttons = result.scalars().all()

        if not buttons:
            return None

        builder = InlineKeyboardBuilder()
        for btn in buttons:
            if btn.button_type == "link":
                answer = await get_answer(btn.button_id)
                if answer and answer.media_url:
                    builder.row(LinkButton(text=btn.button_text, url=answer.media_url))
            else:
                builder.row(CallbackButton(text=btn.button_text, payload=btn.button_id))
        
        # Добавляем кнопку "Назад" или "В меню", если это не главное меню
        if parent_id != "main":
            builder.row(CallbackButton(text="⬅️ Назад", payload="back"))
        
        return builder.as_markup()

# ✅ Обработчик callback (нажатие кнопок)
@dp.message_callback()
async def on_callback(event: MessageCallback):
    payload = event.callback.payload

    # Обработка кнопки "Назад"
    if payload == "back":
        # Для простоты всегда возвращаем в главное меню
        keyboard = await get_keyboard("main")
        await event.message.answer("🏠 Главное меню:", attachments=[keyboard])
        await event.answer()
        return

    # Проверяем, есть ли подменю
    if await has_children(payload):
        keyboard = await get_keyboard(payload)
        await event.message.answer("Выберите раздел:", attachments=[keyboard])
        await event.answer()
        return

    # Обычный ответ
    answer = await get_answer(payload)
    if answer:
        if answer.answer_type == "text":
            await event.message.answer(answer.answer_text)
        elif answer.answer_type == "link" and answer.media_url:
            await event.message.answer(
                answer.answer_text or "Ссылка:",
                attachments=[InlineKeyboardBuilder().row(LinkButton(text="Перейти", url=answer.media_url)).as_markup()]
            )
        await event.answer()
    else:
        await event.message.answer("❌ Ответ не найден")
        await event.answer()

# Обработчик кнопки "Начать"
@dp.bot_started()
async def on_bot_started(event: BotStarted):
    keyboard = await get_keyboard("main")
    await event.bot.send_message(
        chat_id=event.chat_id,
        text="👋 Привет! Добро пожаловать в Бот Первокурсника.",
        attachments=[keyboard]
    )

# Обработчик команды /start
@dp.message_created(Command("start"))
async def on_start(event: MessageCreated):
    keyboard = await get_keyboard("main")
    if keyboard:
        await event.message.answer("🏠 Главное меню:", attachments=[keyboard])
    else:
        await event.message.answer("🏠 Главное меню\n\nБаза данных пуста.")

async def main():
    await init_db()
    await seed_db()
    await bot.delete_webhook()
    print("🤖 Бот запущен и готов к работе!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())