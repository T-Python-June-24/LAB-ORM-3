from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout as auth_logout
from django.conf import settings
from django.utils.module_loading import import_module



def is_admin(user):
    return user.is_authenticated and user.is_staff

@login_required
@user_passes_test(is_admin)
def home(request):
    return render(request, 'home.html')

@login_required
@user_passes_test(is_admin)
def dashboard(request):
    return render(request, 'home.html')

def logout_view(request):
    # Get the current session key before logout
    session_key = request.session.session_key
    
    # Perform logout
    auth_logout(request)
    
    # If there was a session, cycle the session key
    if session_key:
        engine = import_module(settings.SESSION_ENGINE)
        request.session = engine.SessionStore(session_key)
        request.session.cycle_key()
        request.session.save()
    
    return redirect('login')