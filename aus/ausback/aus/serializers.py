from rest_framework import serializers
from .models import *

#Serializers define the API respresentation.

class audioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = audio
        fields = '__all__'

class activeHeartAudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = activeHeartAudio
        fields = '__all__'

class activeLungAudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = activeLungAudio
        fields = '__all__'

class audioListSerializer(serializers.ModelSerializer):
    class Meta:
        model = audioList
        fields = '__all__'

class audioListContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = listContent
        fields = '__all__'