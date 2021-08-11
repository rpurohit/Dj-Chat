# chatapp/views.py
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserLoginForm, UserRegisterForm
from django.shortcuts import render, redirect
from django.urls import reverse

# Login function
def login_view(request):
    '''
        This function is used to validate the user data and redirect the user
        to the index page if the user is authenticated 
        and if not display the error message.
    '''
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        
        if next:
        
            return redirect(next)
        
        return redirect(reverse('chatapp:select_room'))

    context = {
        'form': form,
    }
    
    return render(request, "login.html", context)

# Registration function
def register_view(request):
    '''
        This function is used to register new users.
    '''
    next = request.GET.get('next')
    form = UserRegisterForm(request.POST or None)
    
    if form.is_valid():
    
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
    
        if next:
    
            return redirect(next)
    
        return redirect(reverse('login'))

    context = {
        'form': form,
    }
    
    return render(request, "register.html", context)

# Logout function
def logout_view(request):
    '''
        This function is used to log out the user.
    '''
    logout(request)
    
    return redirect(reverse('login'))

# Room selection function
@login_required
def select_room(request):
    '''
        This function is redirecting the user to the index page.
    '''
    return render(request, 'index.html', {})

# Enter room function
@login_required
def room(request, room_name):
    '''
        This function is used to connect users to the room.
    '''
    return render(request, 'chat.html', {
        'room_name': room_name,
        'user_name': request.user.username
    })

# Redirection function
def redirect_url(request):
    '''
        This function redirecting the user to the index page 
        or login page depending on their authentication.
    '''
    if str(request.user) != 'AnonymousUser':
    
        return redirect(reverse('chatapp:select_room'))        
    
    return redirect(reverse('login'))