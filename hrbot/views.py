"""The module is used to create views."""

from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import viewsets

from .serializers import TicketSerializer
from .models import Ticket


class ChatterBotAppView(LoginRequiredMixin, TemplateView):
    """The class tells the view which template to load."""

    login_url = '/admin/'
    template_name = "app.html"


class TicketView(LoginRequiredMixin, viewsets.ModelViewSet):
    """Class for Ticket APIs."""
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
