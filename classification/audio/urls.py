from django.urls import path
from .views import SaveAttemptAudioView,PredictionView
urlpatterns=[
    path('save/<str:select>/<int:index>',SaveAttemptAudioView.as_view(),name="save"),
    path('prediction',PredictionView.as_view(),name="predict"),
    
]