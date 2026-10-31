import asyncio
import os
from sqlalchemy import text
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

# Импорты для maxapi
from maxapi import Bot, Dispatcher, F
from maxapi.filters.command import Command
from maxapi.types import MessageCreated, BotStarted, MessageCallback
from maxapi.types import CallbackButton, LinkButton
from maxapi.utils.inline_keyboard import InlineKeyboardBuilder

load_dotenv()
BOT_TOKEN = os.getenv("MAX_BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./bot.db")

# SQLite не поддерживает некоторые параметры пула, но базово работает так:
engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

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
    """Автоматическое заполнение базы при первом запуске"""
    async with AsyncSessionLocal() as db:
        # Проверяем, есть ли уже кнопки в базе
        result = await db.execute(text("SELECT COUNT(*) FROM buttons"))
        count = result.scalar()
        
        if count > 0:
            print("✅ База данных уже заполнена, пропускаем сидирование.")
            return

        print("⏳ База пуста. Заполняем начальными данными...")
        
        # Проверяем, есть ли файл seed.sql в папке с проектом
        if os.path.exists("seed.sql"):
            with open("seed.sql", "r", encoding="utf-8") as f:
                sql_script = f.read()
            
            # Выполняем скрипт (разбиваем по точкам с запятой для SQLite)
            # В SQLite нельзя выполнить несколько запросов сразу через execute
            for statement in sql_script.split(";"):
                if statement.strip():
                    await db.execute(text(statement))
            await db.commit()
            print("✅ База данных успешно заполнена!")
        else:
            print("❌ Файл seed.sql не найден. База останется пустой.")

async def get_answer(button_id: str):
    async with AsyncSessionLocal() as db:
        stmt = select(Answer).where(
            Answer.button_id == button_id,
            Answer.is_active == True
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()


async def has_children(button_id: str) -> bool:
    """Проверяет, есть ли у кнопки дочерние элементы (подменю)"""
    async with AsyncSessionLocal() as db:
        stmt = select(Button).where(
            Button.parent_menu == button_id,
            Button.is_active == True
        )
        result = await db.execute(stmt)
        return result.scalars().first() is not None


async def get_submenu_keyboard(parent_id: str):
    """Универсальная функция для построения подменю"""
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
            # Проверяем тип кнопки: ссылка или callback
            answer = await get_answer(btn.button_id)
            if btn.button_type == "link" and answer and answer.media_url:
                builder.row(LinkButton(text=btn.button_text, url=answer.media_url))
            else:
                builder.row(CallbackButton(text=btn.button_text, payload=btn.button_id))

        return builder.as_markup()


async def get_main_keyboard():
    async with AsyncSessionLocal() as db:
        stmt = select(Button).where(
            Button.is_active == True,
            Button.parent_menu == "main"
        ).order_by(Button.order)
        result = await db.execute(stmt)
        buttons = result.scalars().all()

        if not buttons:
            return None

        builder = InlineKeyboardBuilder()
        current_row = []
        for i, btn in enumerate(buttons):
            current_row.append(CallbackButton(text=btn.button_text, payload=btn.button_id))
            if (i + 1) % 2 == 0:
                builder.row(*current_row)
                current_row = []
        if current_row:
            builder.row(*current_row)

        return builder.as_markup()


# ✅ Универсальный обработчик callback
@dp.message_callback()
async def on_callback(event: MessageCallback):
    payload = event.callback.payload

    # Проверяем, есть ли у кнопки дочерние элементы (подменю)
    if await has_children(payload):
        keyboard = await get_submenu_keyboard(payload)
        if keyboard:
            await event.message.answer("Выберите раздел:", attachments=[keyboard])
            await event.answer()
            return

    # Если подменю нет — показываем обычный ответ из БД
    answer = await get_answer(payload)
    if answer:
        if answer.answer_type == "text":
            await event.message.answer(answer.answer_text)
        elif answer.answer_type == "link" and answer.media_url:
            await event.message.answer(
                answer.answer_text or "Ссылка:",
                attachments=[LinkButton(text="Перейти", url=answer.media_url)]
            )
        else:
            await event.message.answer(answer.answer_text)
        await event.answer()
    else:
        await event.message.answer("❌ Ответ не найден")
        await event.answer()


# Обработчик кнопки "Начать"
@dp.bot_started()
async def on_bot_started(event: BotStarted):
    await event.bot.send_message(
        chat_id=event.chat_id,
        text="Привет! Отправь мне /start"
    )


# Обработчик команды /start
@dp.message_created(Command("start"))
async def on_start(event: MessageCreated):
    keyboard = await get_main_keyboard()
    if keyboard:
        await event.message.answer("🏠 Главное меню:", attachments=[keyboard])
    else:
        await event.message.answer("🏠 Главное меню\n\nДобавьте кнопки через БД")


async def main():
    await init_db()
    await seed_db() 
    await bot.delete_webhook()
    print("🤖 Бот запущен и готов к работе!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())