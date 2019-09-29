from django.db import models
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import datetime
##creating a user defined field 
class AudioFileField(models.FileField):
    def __init__(self, *args, **kwargs):
        self.content_types = kwargs.pop("content_types", ['audio/wav', ])
        self.max_upload_size = kwargs.pop("max_upload_size", 10485760) 

        super(AudioFileField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super(AudioFileField, self).clean(*args, **kwargs)

        file = data.file
        content_type = file.content_type
        assert content_type in self.content_types, "File type not supported"
        #assert file._size > self.max_upload_size, "File too large"
        return data


class AudioManager(models.Manager):
    def create_attempt(self, blob):
        attempt = AudioModel()
        attempt.audio_file = SimpleUploadedFile(datetime.now().strftime("%d%m%y%H%M%S.wav"), blob)
        attempt.save()
        return attempt

class AudioModel(models.Model):
   audio_file = AudioFileField(null=True, upload_to='audio/')
   timestamp = models.DateTimeField(auto_now_add=True, null=True)
   prediction = models.CharField(max_length=20,null=True)
   response = models.BooleanField(default = False)
   #TODO: Store user response also
   objects = AudioManager()