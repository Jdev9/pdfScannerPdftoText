from django.db import models
from django.contrib.auth.models import User


class Upload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to="uploads/")

    def __str__(self):
        return self.file.name

    
class TextData(models.Model):
    text = models.OneToOneField(Upload, on_delete=models.CASCADE)
    data = models.TextField()

    def __str__(self):
        return self.text.file.name