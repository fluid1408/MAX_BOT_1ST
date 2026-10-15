from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Button(Base):
    __tablename__ = "buttons"
    
    id = Column(Integer, primary_key=True, index=True)
    button_id = Column(String(50), unique=True, nullable=False, index=True)  # "contacts"
    button_text = Column(String(100), nullable=False)  # "📞 Контакты"
    button_type = Column(String(20), default="callback")  # callback, command, inline
    parent_menu = Column(String(50), default="main")  # main, submenu
    order = Column(Integer, default=0)  # порядок отображения
    is_active = Column(Boolean, default=True)
    
    # Связь с ответами (один ко многим)
    answers = relationship("Answer", back_populates="button")


class Answer(Base):
    __tablename__ = "answers"
    
    id = Column(Integer, primary_key=True, index=True)
    button_id = Column(String(50), ForeignKey("buttons.button_id"), nullable=False)
    answer_text = Column(Text, nullable=False)
    answer_type = Column(String(20), default="text")  # text, photo, video
    media_url = Column(String(500), nullable=True)  # ссылка на файл
    is_active = Column(Boolean, default=True)
    
    # Связь с кнопкой
    button = relationship("Button", back_populates="answers")