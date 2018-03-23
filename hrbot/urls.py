"""The module contains urls for views."""

from django.urls import include, path
# from rest_framework.urlpatterns import format_suffix_patterns
# from django.contrib import admin
from .views import ChatterBotAppView, render_faq, bot_login, login_proc

# urlpatterns = [
#     url(r'^$', ChatterBotAppView.as_view(), name='main'),
#     # url(r'^admin/', include(admin.site.urls), name='admin'),
#     url(r'^api/chatterbot/', include(chatterbot_urls,
# namespace='chatterbot')),
# ]
urlpatterns = [
    path('', ChatterBotAppView.as_view(), name='main'),
    path('faq/', render_faq, name='faq'),
    # path('login/', bot_login, name='faq'),
    # path('login/proc/', login_proc, name='faq'),
    # url(r'^$', ChatterBotAppView.as_view(), name='main'),
    # url(r'^admin/', include(admin.site.urls), name='admin'),
    # url(r'^api/chatterbot/', include(chatterbot_urls,
    # namespace='chatterbot')),
    path('chatterbot/', include('chatterbot.ext.django_chatterbot.urls',
                                namespace='chatterbot')),
    # path('leave/apply', CreateView.as_view(), name='leave_apply'),
]

# urlpatterns = format_suffix_patterns(urlpatterns)
