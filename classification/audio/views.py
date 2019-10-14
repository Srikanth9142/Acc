from django.shortcuts import render
from django.http import HttpResponse;
from rest_framework.parsers import BaseParser
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from .models import AudioModel
from audio.serializers import PredictionSerializer
from audio.mlcode import create_model
from audio.mlcode import predictAccent
from audio.mlcode import predictAudio
# Create your views here.
"""
handle binary audio file upload that rest server is unable to parse by default
"""
class AudioParser(BaseParser):
    media_type = 'application/octet-stream'
    def parse(self, stream, media_type='application/octet-stream', parser_context=None):
        return stream.read()

"""
Save user attempt for a question
"""
Audioid=0
Audioid1=0
class SaveAttemptAudioView(APIView):
    parser_classes = (AudioParser,)

    def post(self, request):
        try:
            attempt,name = AudioModel.objects.create_attempt(request.data)
            accent_str = predictAudio(name)
            attempt.prediction=accent_str
            attempt.save()
            global Audioid
            Audioid = attempt.pk
            Audioid1 = attempt.pk
            print("Audio Id :",Audioid)
            print("Accent is as :",attempt.prediction)
            # create a serializer for prediction
            # and return the prediction
            return Response({'prediction':0}, status=201)
        except Exception as e:
            print(e)
            return Response({"result":"error"}, status=400)
def save(request):
    return HttpResponse("hai this will save!!")

def printPredict(request):
    global Audioid1
    pr = AudioModel.objects.filter(pk=Audioid1).values('prediction')
    print("Printing in printPredict")
    print(Audioid1)
    return HttpResponse("see terminal")

class PredictionView(generics.ListCreateAPIView):
    queryset = AudioModel.objects.all()
    serializer_class = PredictionSerializer

