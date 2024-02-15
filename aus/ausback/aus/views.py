from django.shortcuts import render
# need http response to return json response
from django.http import JsonResponse
# use rest fraomework for views
from rest_framework import viewsets, status
# import audio model serializer
from .serializers import audioSerializer,activeHeartAudioSerializer,activeLungAudioSerializer, audioListSerializer, audioListContentSerializer
# import the following models
from .models import *
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework.routers import DefaultRouter
# for delete list content
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from urllib.parse import unquote
# for get audio file
import os
from django.http import FileResponse
from django.views import View
from django.conf import settings
# for edit and remove function of audio
from rest_framework.decorators import action
from rest_framework.response import Response
# for add audio to the storage
from django.core.files.storage import default_storage
from django.views.decorators.http import require_POST
# for delete audio file
from django.views.decorators.http import require_http_methods
# for User login
from django.contrib.auth.models import AbstractUser
from django.db import models

# a simple home page view
def home(request):
    # You can add any additional context data you want to pass to the template here
    context = {
        'page_title': 'Welcome to Our Website',
        'welcome_message': 'Hello, and welcome to our website!',
    }
    return render(request, 'home.html', context)

class audioViewSet(viewsets.ModelViewSet):
    # define queryset
    queryset = audio.objects.all().order_by('audio_id')
    # define serializer class
    serializer_class = audioSerializer

    @action(detail=True, methods=['patch'])
    def update_audio_property(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    @action(detail=True, methods=['delete'])
    def delete_audio(self, request, pk=None):
        try:
            instance = self.get_object()
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

class activeHeartAudioViewSet(viewsets.ModelViewSet):
    # define queryset
    queryset = activeHeartAudio.objects.all().order_by('heart_audio_id')
    # define serializer class
    serializer_class = activeHeartAudioSerializer

class activeLungAudioViewSet(viewsets.ModelViewSet):
    # define queryset
    queryset = activeLungAudio.objects.all().order_by('lung_audio_id')
    # define serializer class
    serializer_class = activeLungAudioSerializer

class audioListViewSet(viewsets.ModelViewSet):
    # define queryset
    queryset = audioList.objects.all().order_by('list_id')
    # define serializer class
    serializer_class = audioListSerializer

class audioListContentViewSet(viewsets.ModelViewSet):
    # define queryset
    queryset = listContent.objects.all().order_by('content_id')
    # define serializer class
    serializer_class = audioListContentSerializer

    @action(detail=True, methods=['delete'])
    def delete_related_content_by_audio_id(self, request, pk=None):
        try:
            audio_id = self.get_object().audio_id
            related_content = listContent.objects.filter(audio_id=audio_id)
            related_content.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

class AudioFileView(View):
    def get(self, request, filename):
        file_path = os.path.join(settings.MEDIA_ROOT, 'audio', filename)
        response = FileResponse(open(file_path, 'rb'))
        return response
    
class CustomUser(View):
    user_log_state = models.CharField(max_length=50, default='')
    user_type = models.CharField(max_length=50, null=True, blank=True)

# Play Random Heart Beat Sounds
def playRandomHeartBeat(request):
    random_heart_beat = audio.objects.filter(audio_type = 'Heartbeat').order_by('?').first()
    if random_heart_beat:
        print(random_heart_beat.audio_link)
        name = random_heart_beat.audio_name
        link = random_heart_beat.audio_link
        response_data = {'audio_name': name, 'audio_link': link}
        return JsonResponse(response_data, safe=False)
    else:
        return JsonResponse({'error': 'No audio found'}, status=404)

# Play Random Abnormal Sounds
def playRandomAbnormal(request):
    random_abnormal = audio.objects.filter(audio_name__contains='Abnormal').order_by('?').first()
    if random_abnormal:
        print(random_abnormal.audio_link)
        name = random_abnormal.audio_name
        type = random_abnormal.audio_type
        link = random_abnormal.audio_link
        response_data = {'audio_name': name,'audio_type': type, 'audio_link': link}
        return JsonResponse(response_data, safe=False)
    else:
        return JsonResponse({'error': 'No audio found'}, status=404)

# Play Random Sounds
def playRandom(request):
    random_audio = audio.objects.all().order_by('?').first()
    if random_audio:
        print(random_audio.audio_link)
        name = random_audio.audio_name
        type = random_audio.audio_type
        link = random_audio.audio_link
        response_data = {'audio_name': name, 'audio_type': type, 'audio_link': link}
        return JsonResponse(response_data, safe=False)
    else:
        return JsonResponse({'error': 'No audio found'}, status=404)

# Get all the audio in the database
def getAllAudio(request):
    audio_list = audio.objects.all()
    audio_dict = {}

    for audio_item in audio_list:
        audio_id = audio_item.audio_id
        audio_name = audio_item.audio_name
        audio_type = audio_item.audio_type
        audio_description = audio_item.audio_description
        audio_level = audio_item.audio_level
        audio_link = audio_item.audio_link
        audio_dict[audio_name] = {
            'audio_id': audio_id,
            'audio_name': audio_name,
            'audio_type': audio_type,
            'audio_description': audio_description,
            'audio_level': audio_level,
            'audio_link': audio_link,
        }
    response_data = [{'audio_name': key, **values} for key, values in audio_dict.items()]
    return JsonResponse(response_data, safe=False)

# Get all the lists in the database
def getAllList(request):
    list_objects = audioList.objects.all()
    list_dict = {}

    for list_item in list_objects:
        list_id = list_item.list_id
        list_name = list_item.list_name

        list_dict[list_id] = {
            'list_id': list_id,
            'list_name': list_name,
        }

    response_data = [{'list_name': key, **values} for key, values in list_dict.items()]
    return JsonResponse(response_data, safe=False)

# Get all the audio in a list
def getAllContent(request):
    content_objects = listContent.objects.all()
    content_dict = {}

    for content_item in content_objects:
        list_id = content_item.list_id
        audio_id = content_item.audio_id

        content_dict[list_id] = {
            'list_id': list_id,
            'audio_id': audio_id,
        }
    
    response_data = [{'list_id': key, **values} for key, values in content_dict.items()]
    return JsonResponse(response_data, safe=False)

# delete a list content
@csrf_exempt
def deleteListContent(request, list_name, audio_name):
    # Decode URL parameters if needed
    list_name = unquote(list_name)
    audio_name = unquote(audio_name)
    listContent.objects.filter(list_name=list_name, audio_name=audio_name).delete()
    return JsonResponse({'message': 'Delete successfully'}, safe=False)

# delete all the list content related to an audio
@csrf_exempt
def deleteRelatedListContent(request, audio_id):
    # Decode URL parameters if needed
    audio_id = unquote(audio_id)
    listContent.objects.filter(audio_id=audio_id).delete()
    return JsonResponse({'message': 'Delete successfully'}, safe=False)

# delete the active heart audio for now
@csrf_exempt
def updateActiveHeartAudio(request, id, list_id):
    # Decode URL parameters if needed
    id = unquote(id)
    list_id = unquote(list_id)
    song = audio.objects.filter(audio_id=id)
    activeHeartAudio.objects.filter(heart_audio_list=list_id).delete()
    activeHeartAudio.objects.create(
        heart_audio_id = song[0].audio_id,
        heart_audio_name = song[0].audio_name,
        heart_audio_type = song[0].audio_type,
        heart_audio_description = song[0].audio_description,
        heart_audio_level = song[0].audio_level,
        heart_audio_link = song[0].audio_link,
        heart_audio_list = list_id,
    )
    return JsonResponse({'message': 'Update successfully'}, safe=False)

# delete the active lung audio for now
@csrf_exempt
def updateActiveLungAudio(request, id, list_id):
    # Decode URL parameters if needed
    id = unquote(id)
    list_id = unquote(list_id)
    song = audio.objects.filter(audio_id=id)
    activeLungAudio.objects.filter(lung_audio_list=list_id).delete()
    activeLungAudio.objects.create(
        lung_audio_id = song[0].audio_id,
        lung_audio_name = song[0].audio_name,
        lung_audio_type = song[0].audio_type,
        lung_audio_description = song[0].audio_description,
        lung_audio_level = song[0].audio_level,
        lung_audio_link = song[0].audio_link,
        lung_audio_list = list_id,
    )
    return JsonResponse({'message': 'Update successfully'}, safe=False)

# Update the list name for all audio related to the list
@csrf_exempt
def updateListContent(request,list_name_before, list_name_after):
    # Decode URL parameters if needed
    list_name_before = unquote(list_name_before)
    list_name_after = unquote(list_name_after)
    contents = listContent.objects.filter(list_name=list_name_before)
    for content in contents:
        content.list_name = list_name_after
        content.save()
    return JsonResponse({'message': 'Update successfully'}, safe=False)

def addAudio(request):
    return JsonResponse({'message':'successfully!'},safe= False)

@csrf_exempt
@require_POST
def uploadAudio(request):
    if 'file' in request.FILES:
        audio_file = request.FILES['file']

        # Save the file to the media/audio folder
        file_path = default_storage.save(f'audio/{audio_file.name}', audio_file)

        return JsonResponse({'success': True, 'filename': file_path})
    else:
        return JsonResponse({'success': False, 'message': 'File upload failed'})

@csrf_exempt    
@require_http_methods(["DELETE"])
def delete_audio_file(request, link):
    try:
        # Assuming that 'link' is the filename (e.g., '005.wav')
        file_path = os.path.join('media', 'audio', link)

        # Check if the file exists before attempting to delete
        if os.path.exists(file_path):
            os.remove(file_path)
            return JsonResponse({'message': 'Audio file deleted successfully.'}, status=200)
        else:
            return JsonResponse({'error': 'File not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
@csrf_exempt
def getActiveHeartAudio(request, list_id):
    list_id = unquote(list_id)
    audio = activeHeartAudio.objects.filter(heart_audio_list=list_id)
    if audio:
        return JsonResponse({'audio_id': audio[0].heart_audio_id}, safe=False)
    else:
        return JsonResponse({'error': 'No audio found for the given list ID'}, status=404)

@csrf_exempt
def getActiveLungAudio(request, list_id):
    list_id = unquote(list_id)
    audio = activeLungAudio.objects.filter(lung_audio_list=list_id)
    if audio:
        return JsonResponse({'audio_id': audio[0].lung_audio_id}, safe=False)
    else:
        return JsonResponse({'error': 'No audio found for the given list ID'}, status=404)
    

@csrf_exempt
def register(request):
    return JsonResponse({'status': 'Success'},safe= False)