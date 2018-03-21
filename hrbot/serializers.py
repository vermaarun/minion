""" Serializer class for model. """
from rest_framework import serializers

from .models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    """Serializer class for Ticket."""
    class Meta:
        model = Ticket
        fields = '__all__'
