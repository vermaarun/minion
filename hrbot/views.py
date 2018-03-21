"""The module is used to create views."""

from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
# from rest_framework import generics
# from .serializers import LeaveDataSerializer
# from .models import LeaveData


class ChatterBotAppView(LoginRequiredMixin, TemplateView):
    """The class tells the view which template to load."""

    login_url = '/admin/'
    template_name = "app.html"


# class CreateView(generics.ListCreateAPIView):
#     """The class defines the create behaviour of leave api."""
#
#     queryset = LeaveData.objects.all()
#     serializer_class = LeaveDataSerializer
#
#     def perform_create(self, serializer):
#         """Save data when creating new leave entry."""
#
#         serializer.save()
