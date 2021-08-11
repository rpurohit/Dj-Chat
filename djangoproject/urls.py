# djangoproject/urls.py
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from chatapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/register/', views.register_view, name='register'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('chat/', include('chatapp.urls'), name='chatapp'),
    path('', views.redirect_url),
]
