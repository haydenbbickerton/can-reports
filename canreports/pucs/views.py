from rest_framework import viewsets, mixins, generics
from rest_framework.decorators import action, api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Puc, CanMessage, GpsMessage
from .serializers import PucSerializer, CanMessageSerializer, GpsMessageSerializer


class PucViewSet(viewsets.ModelViewSet):
    """
    Updates and retrives pucs
    """
    queryset = Puc.objects.all()
    serializer_class = PucSerializer
    permission_classes = (AllowAny,)

class CanMessageViewSet(viewsets.ModelViewSet):
    """
    Updates and retrives CanMessage
    """
    queryset = CanMessage.objects.all().order_by('timestamp')
    serializer_class = CanMessageSerializer
    permission_classes = (AllowAny,)

class GpsMessageViewSet(viewsets.ModelViewSet):
    """
    Updates and retrives GpsMessage
    """
    queryset = GpsMessage.objects.all().order_by('timestamp')
    serializer_class = GpsMessageSerializer
    permission_classes = (AllowAny,)
