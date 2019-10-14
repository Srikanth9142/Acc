from django.urls import path
from .views import SaveAttemptAudioView,PredictionView,printPredict
urlpatterns=[
    path('save',SaveAttemptAudioView.as_view(),name="save"),
    path('prediction',PredictionView.as_view(),name="predict"),
    path('print',printPredict,name="print"),
    
]