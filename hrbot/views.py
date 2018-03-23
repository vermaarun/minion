"""The module is used to create views."""

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.generic.base import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets

from .serializers import TicketSerializer
from .models import Ticket

@csrf_exempt
def login_proc(request):
    logout(request)

    data = request.POST.copy()

    email = data.get('username', '')
    password = data.get('password', '')
    print(email)
    if not email or not password:
        return HttpResponseRedirect('/login/')

    user = authenticate(username=email, password=password)
    login(request, user)
    redirect_url = '/api/'
    response = HttpResponseRedirect(redirect_url)
    return response
    

def bot_login(request):
    #if request.user.is_authenticated():
    #    return HttpResponseRedirect('/api/')

    return render_to_response('login.html')


def bot_logout(request):
    logout(request)
    return render_to_response('logout.html')


def render_faq(request):
    return render(request, 'faq.html', {})


class ChatterBotAppView(LoginRequiredMixin, TemplateView):
    """The class tells the view which template to load."""

    login_url = '/admin/'
    template_name = "app.html"


class TicketView(LoginRequiredMixin, viewsets.ModelViewSet):
    """Class for Ticket APIs."""
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
