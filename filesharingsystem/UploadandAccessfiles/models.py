from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Files(models.Model):
    pdf = models.FileField(upload_to='store/pdfs/')

    def __str__(self):
        return self.pdf
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    verification_token = models.CharField(max_length=32, blank=True)