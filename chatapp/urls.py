# chatapp/urls.py
from django.urls import path

#chatapp/urls.py
from . import views

app_name = 'chatapp'

urlpatterns = [
    # ex: /chat
    path('', views.login_view, name='index'),
    # ex: /chat/room
    path('room', views.select_room, name='select_room'),
    # ex: /chat/roomname
    path('<str:room_name>/', views.room, name='room'),
]