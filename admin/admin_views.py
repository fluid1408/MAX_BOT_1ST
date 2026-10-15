from fastapi_admin.widgets import Text, Textarea, Boolean, Integer
from bot.models import Button, Answer

class ButtonAdmin(ModelAdmin):
    model = Button
    icon = "fas fa-keyboard"
    list_display = ["id", "button_id", "button_text", "parent_menu", "order", "is_active"]
    fields = ["button_id", "button_text", "button_type", "parent_menu", "order", "is_active"]
    search_fields = ["button_id", "button_text"]
    
    # Виджеты для формы редактирования
    form_widgets = {
        "button_id": Text(),
        "button_text": Text(),
        "button_type": Text(),
        "parent_menu": Text(),
        "order": Integer(),
        "is_active": Boolean(),
    }

class AnswerAdmin(ModelAdmin):
    model = Answer
    icon = "fas fa-reply"
    list_display = ["id", "button_id", "answer_text", "answer_type", "is_active"]
    fields = ["button_id", "answer_text", "answer_type", "media_url", "is_active"]
    search_fields = ["button_id", "answer_text"]
    
    form_widgets = {
        "button_id": Text(),
        "answer_text": Textarea(),
        "answer_type": Text(),
        "media_url": Text(),
        "is_active": Boolean(),
    }