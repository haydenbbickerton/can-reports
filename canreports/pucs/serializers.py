from rest_framework import serializers
from .models import Puc, CanMessage, GpsMessage


class PucSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Puc
        fields = ('id', 'uuid')


class CanMessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CanMessage
        fields = ('id', 'puc', 'header', 'dlc', 'payload', 'timestamp')


class GpsMessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GpsMessage
        fields = ('id', 'puc', 'latitude', 'longitude', 'groundspeed', 'truecourse', 'timestamp')
