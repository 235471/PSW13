from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.messages import constants
from django.http import Http404
from django.contrib.auth.decorators import login_required as django_login_required
from .auth import validate_token
from .models import Mentorship, Task

def mentee_token_required(view_func):
    """
    Decorator for views requiring a valid mentee token from cookies.
    Redirects to 'auth_mentee' if token is missing or invalid.
    Attaches the validated mentee object to request.mentee.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        token = request.COOKIES.get('auth_token')
        if not token:
            messages.add_message(request, constants.ERROR, 'Please inform your access token.')
            return redirect('auth_mentee') 

        mentee = validate_token(token)
        if not mentee:
            messages.add_message(request, constants.ERROR, 'Invalid token')
            return redirect('auth_mentee')

        request.mentee = mentee 
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def mentor_owns_mentee_required(view_func):
    """
    Decorator for views requiring the logged-in user to be the mentor 
    of the mentee specified by the 'id' parameter in the URL.
    Also ensures the user is logged in.
    Attaches the validated mentee object to request.mentee.
    """
    @wraps(view_func)
    def _wrapped_view(request, id, *args, **kwargs):
        if not request.user.is_authenticated:
            return django_login_required(lambda r, *a, **k: None)(request) 

        try:
            mentee = Mentorship.objects.get(id=id)
        except Mentorship.DoesNotExist:
            raise Http404('Mentee not found.')

        if mentee.user != request.user:
            raise Http404('You are not authorized to access this page.')

        request.mentee = mentee
        return view_func(request, id, *args, **kwargs)
    return _wrapped_view

def mentor_owns_task_mentee_required(view_func): 
    """
    Decorator for views requiring the logged-in user to be the mentor 
    of the mentee associated with the task specified by the 'id' parameter.
    Also ensures the user is logged in.
    Attaches the validated task object to request.task.
    """
    @wraps(view_func)
    def _wrapped_view(request, id, *args, **kwargs):
        if not request.user.is_authenticated:
            return django_login_required(lambda r, *a, **k: None)(request) 

        try:
            task = Task.objects.get(id=id)
        except Task.DoesNotExist:
            raise Http404('Task not found.')

        if task.mentee.user != request.user:
            raise Http404('You are not authorized to modify this task.')

        request.task = task
        return view_func(request, id, *args, **kwargs)
    return _wrapped_view

def task_status_checks_required(view_func):
    """
    Decorator specifically for the task_status view.
    Checks:
    1. User is authenticated.
    2. Mentee auth token is valid.
    3. Logged-in user is the mentor for the task's mentee.
    Attaches the validated task object to request.task.
    """
    @wraps(view_func)
    def _wrapped_view(request, id, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request, constants.ERROR, 'Please login to continue.')
            return redirect('login') 

        # Check token - kept from original view logic
        token = request.COOKIES.get('auth_token')
        if not token:
            messages.add_message(request, constants.ERROR, 'Please inform your access token.')
            return redirect('auth_mentee')

        mentee_from_token = validate_token(token)
        if not mentee_from_token:
            messages.add_message(request, constants.ERROR, 'Invalid token')
            return redirect('auth_mentee')
            
        try:
            task = Task.objects.get(id=id)
        except Task.DoesNotExist:
            raise Http404('Task not found.')

        if task.mentee.user != request.user:
            raise Http404('You are not authorized to modify this task.')
            
        # Optional check: Does the token belong to the same mentee as the task?
        # This might be overly strict depending on requirements.
        # if task.mentee != mentee_from_token:
        #     raise Http404('Token does not match task mentee.')

        request.task = task
        return view_func(request, id, *args, **kwargs)
    return _wrapped_view
