from django.shortcuts import render
from django.http import HttpResponse;
from rest_framework.parsers import BaseParser
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import AudioModel
from audio.serializers import PredictionSerializer
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
class SaveAttemptAudioView(APIView):
    parser_classes = (AudioParser,)

    def post(self, request):
        try:
            attempt = AudioModel.objects.create_attempt(request.data)
            # do your predictions
            # update attempt model with the prediction and save it
            # create a serializer for prediction
            # and return the prediction
            return Response({'course': 0}, status=201)
        except Exception as e:
            print(e)
            return Response({"result":"error"}, status=400)
def save(request):
    return HttpResponse("hai this will save!!")