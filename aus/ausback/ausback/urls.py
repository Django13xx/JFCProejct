"""
URL configuration for ausback project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include #import include
from rest_framework import routers
from django.contrib.auth.views import LoginView, LogoutView
from aus.views import *

#define the routers
router = routers.DefaultRouter()
router.register('audio', audioViewSet,basename='audio') # register the audio viewset
router.register('activeHeartAudio', activeHeartAudioViewSet,basename='activeHeartAudio') # register the audio viewset
router.register('activeLungAudio', activeLungAudioViewSet,basename='activeLungAudio') # register the audio viewset
router.register('audioList', audioListViewSet,basename='audioList') # register the audio viewset
router.register('listContent', audioListContentViewSet,basename='listContent') # register the audio viewset

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),  # 登录页面
    path('logout/', LogoutView.as_view(), name='logout'),  # 注销页面
    path('register/', register, name='register'),  # 注册页面
    path('api/', include(router.urls)), # include the router urls
    path('api/playRandomHeartBeat/', playRandomHeartBeat, name= 'playRandomHeartBeat'),
    path('api/playRandomAbnormal/', playRandomAbnormal, name= 'playRandomAbnormal'),
    path('api/playRandom/', playRandom, name= 'playRandom'),
    path('api/getAllAudio/', getAllAudio, name='getAllAudio'),
    path('api/getAllList/', getAllList, name='getAllList'),
    path('api/getAllContent/', getAllContent, name='getAllContent'),
    path('api/deleteListContent/<str:list_name>/<str:audio_name>/', deleteListContent, name='deleteListContent'),
    path('api/deleteRelatedListContent/<str:audio_id>/', deleteRelatedListContent, name='deleteRelatedListContent'),
    path('api/updateListContent/<str:list_name_before>/<str:list_name_after>/', updateListContent, name='updateListContent'),
    path('api/updateActiveHeartAudio/<str:id>/<str:list_id>/', updateActiveHeartAudio, name='updateActiveHeartAudio'),
    path('api/updateActiveLungAudio/<str:id>/<str:list_id>/', updateActiveLungAudio, name='updateActiveLungAudio'),
    path('api/addAudio/',addAudio, name='addAudio'),
    path('api/audioFile/<str:filename>/', AudioFileView.as_view(), name='audio-file'),
    path('api/uploadAudio/', uploadAudio, name='uploadAudio'),
    path('api/audioFile/<str:link>/delete_audio_file/', delete_audio_file, name='delete_audio_file'),
    path('api/getActiveHeartAudio/<str:list_id>/', getActiveHeartAudio, name='getActiveHeartAudio'),
    path('api/getActiveLungAudio/<str:list_id>/', getActiveLungAudio, name='getActiveLungAudio'), 
]
