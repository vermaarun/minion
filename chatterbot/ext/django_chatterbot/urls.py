from django.conf.urls import url
from .views import ChatterBotView

app_name = 'django_chatterbot'
urlpatterns = [
    url(
        r'^$',
        ChatterBotView.as_view(),
        name='chatterbot',
    ),
]
