from django.db import models
from django.http import HttpResponse
# for login function
from django.contrib.auth.models import AbstractUser

# Create your models here.
# create a audio link model
class audio(models.Model):
    audio_id = models.IntegerField (primary_key=True)
    audio_name = models.CharField(max_length=200)
    audio_type = models.CharField(max_length=20, default='undefined')
    audio_description = models.CharField(max_length=500, default='')
    audio_level = models.CharField(max_length=20, default='All levels')
    audio_link = models.CharField(max_length=200)
    def __str__(self):
        return self.audio_name
    
class activeHeartAudio(models.Model):
    id = models.AutoField(primary_key=True)
    heart_audio_id = models.IntegerField (default=0)
    heart_audio_name = models.CharField(max_length=200)
    heart_audio_type = models.CharField(max_length=20, default='undefined')
    heart_audio_description = models.CharField(max_length=500, default='')
    heart_audio_level = models.CharField(max_length=20, default='All levels')
    heart_audio_link = models.CharField(max_length=200)
    heart_audio_list = models.IntegerField(default=0)
    def __str__(self):
        return self.heart_audio_name
    
class activeLungAudio(models.Model):
    id = models.AutoField(primary_key=True)
    lung_audio_id = models.IntegerField (default=0)
    lung_audio_name = models.CharField(max_length=200)
    lung_audio_type = models.CharField(max_length=20, default='undefined')
    lung_audio_description = models.CharField(max_length=500, default='')
    lung_audio_level = models.CharField(max_length=20, default='All levels')
    lung_audio_link = models.CharField(max_length=200)
    lung_audio_list = models.IntegerField(default=0)
    def __str__(self):
        return self.lung_audio_name
class CustomUser(AbstractUser):
    user_id = models.IntegerField(primary_key=True, default=1)
    user_name = models.CharField(max_length=200)
    user_password = models.CharField(max_length=20)
    user_log_state = models.BooleanField(default=False)

    def __str__(self):
        return self.user_name
    
class user(models.Model):
    user_id = models.IntegerField (primary_key= True) # primary_key is the only reference
    user_name = models.CharField (max_length= 200) # length of byte
    user_password = models.CharField (max_length= 20)
    user_log_state = models.BooleanField (default= False) # The initial state of user set as false
    def __str__(self):
        return self.user_name

class question(models.Model):
    question_id = models.IntegerField(primary_key = True)

class audioList(models.Model):
    list_id = models.AutoField(primary_key=True)
    list_name = models.CharField(max_length=200)
    def __str__(self):
        return f"List {self.list_id}"

class listContent(models.Model):
    content_id = models.AutoField(primary_key=True)
    list_id = models.IntegerField(default=0)
    list_name = models.CharField(max_length=200)
    audio_id = models.IntegerField(default=0)
    audio_name = models.CharField(max_length=200)
    def __str__(self):
        return f"List {self.list_id} Content {self.content_id}"