from django.urls import path
from .views import SaveAttemptAudioView
urlpatterns=[
    path('save',SaveAttemptAudioView.as_view(),name="save"),
]