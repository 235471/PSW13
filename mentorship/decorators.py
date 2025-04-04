from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.messages import constants
from django.http import Http404
from django.contrib.auth.decorators import login_required as django_login_required
from .auth import validate_token
from .models import Mentorship, Task

# Decorator for views requiring a valid mentee token from cookies
def mentee_token_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        token = request.COOKIES.get('auth_token')
        if not token:
            messages.add_message(request, constants.ERROR, 'Please inform your access token.')
            return redirect('auth_mentee') # URL name confirmed from urls.py

        mentee = validate_token(token)
        if not mentee:
            messages.add_message(request, constants.ERROR, 'Invalid token')
            return redirect('auth_mentee')

        # Add mentee to request object for easy access in the view if needed,
        # but don't change the view signature.
        request.mentee = mentee 
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# Decorator for views where the logged-in user must be the mentor of the mentee specified by 'id'
# This decorator also implicitly requires login.
def mentor_owns_mentee_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, id, *args, **kwargs):
        # Ensure user is logged in first
        if not request.user.is_authenticated:
            # Redirects to login URL defined in settings.LOGIN_URL
            return django_login_required(lambda r, *a, **k: None)(request) 

        try:
            mentee = Mentorship.objects.get(id=id)
        except Mentorship.DoesNotExist:
            raise Http404('Mentee not found.')

        if mentee.user != request.user:
            # User is logged in, but doesn't own this mentee
            raise Http404('You are not authorized to access this page.')

        # Add mentee to request object for easy access in the view if needed.
        request.mentee = mentee
        # Pass the original 'id' parameter as the view expects it.
        return view_func(request, id, *args, **kwargs)
    return _wrapped_view

# Decorator for task status update: logged-in user must be the mentor of the task's mentee
# This decorator also implicitly requires login.
def mentor_owns_task_mentee_required(view_func): # Renamed for clarity
    @wraps(view_func)
    def _wrapped_view(request, id, *args, **kwargs):
         # Ensure user is logged in first
        if not request.user.is_authenticated:
            return django_login_required(lambda r, *a, **k: None)(request) 

        try:
            task = Task.objects.get(id=id)
        except Task.DoesNotExist:
            raise Http404('Task not found.')

        # Check if the logged-in user is the mentor associated with this task's mentee
        if task.mentee.user != request.user:
            raise Http404('You are not authorized to modify this task.')

        # Add task to request object for easy access in the view if needed.
        request.task = task
        # Pass the original 'id' parameter as the view expects it.
        return view_func(request, id, *args, **kwargs)
    return _wrapped_view

# Decorator specifically for task_status view which also needs token validation
# Combines mentee_token_required and checks if the logged-in user owns the task's mentee
def task_status_checks_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, id, *args, **kwargs):
        # 1. Check login
        if not request.user.is_authenticated:
            messages.add_message(request, constants.ERROR, 'Please login to continue.')
            # Assuming 'login' is the name of your login URL
            return redirect('login') 

        # 2. Check token (although maybe redundant if only mentors access this?)
        # Let's keep it as per original logic for now.
        token = request.COOKIES.get('auth_token')
        if not token:
            messages.add_message(request, constants.ERROR, 'Please inform your access token.')
            return redirect('auth_mentee')

        mentee_from_token = validate_token(token)
        if not mentee_from_token:
            messages.add_message(request, constants.ERROR, 'Invalid token')
            return redirect('auth_mentee')
            
        # 3. Fetch Task and check ownership via mentee
        try:
            task = Task.objects.get(id=id)
        except Task.DoesNotExist:
            raise Http404('Task not found.')

        # Check if the logged-in user is the mentor associated with this task's mentee
        if task.mentee.user != request.user:
            raise Http404('You are not authorized to modify this task.')
            
        # Optional: Check if mentee from token matches task's mentee?
        # if task.mentee != mentee_from_token:
        #     messages.add_message(request, constants.ERROR, 'Token does not match task mentee.')
        #     return redirect('auth_mentee') # Or raise Http404

        # Add task to request object
        request.task = task
        return view_func(request, id, *args, **kwargs)
    return _wrapped_view
