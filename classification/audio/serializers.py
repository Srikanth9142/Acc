from rest_framework import serializers
from .models import AudioModel

class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioModel
        fields=('prediction','response')
