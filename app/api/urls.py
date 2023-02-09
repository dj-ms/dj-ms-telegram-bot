from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from app.api.views import telegram_views

urlpatterns = [
    # path('__debug__/', include(debug_toolbar.urls)),
    path('super_secter_webhook/', csrf_exempt(telegram_views.TelegramBotWebhookView.as_view())),
]
