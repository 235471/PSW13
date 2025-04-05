from datetime import datetime, timedelta
from datetime import datetime, timedelta
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from mentorship.models import Mentorship
from .models import AppointmentAvailability, Meeting, Mentorship, Navigator, Task, Upload
from .decorators import mentee_token_required, mentor_owns_mentee_required, task_status_checks_required 
from django.contrib import messages
from django.contrib.messages import constants
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

@login_required
def mentorship(request):  
    if request.method == 'GET':
        mentees = Mentorship.objects.filter(user=request.user)
        navigators = Navigator.objects.filter(user=request.user)

        stages_flat = []
        stages_count = []

        for i, j in Mentorship.stage_choices:
            count = Mentorship.objects.filter(stage=i).filter(user=request.user).count()
            if count > 0:
                stages_flat.append(j)
                stages_count.append(count)

        return render(request, 'mentorship.html', {
            'stages': Mentorship.stage_choices,
            'stages_flat': stages_flat,
            'stages_count': stages_count,
            'navigators': navigators,
            'mentees': mentees
            })
    elif request.method == 'POST':
        name = request.POST.get('name')
        photo = request.FILES.get('photo')
        stage = request.POST.get('stage')
        navigator = request.POST.get('navigator')

        try:
            navigator = Navigator.objects.get(id=navigator)
        except Navigator.DoesNotExist:
            messages.add_message(request, constants.ERROR, 'Navigator not found.')
            return redirect('mentorship')

        mentor = Mentorship(
            name=name, 
            photo=photo,  
            stage=stage, 
            navigator=navigator,
            user = request.user
        )

        mentor.save()
        messages.add_message(request, constants.SUCCESS, 'Mentee registered successfully')
        return redirect('mentorship')

@login_required        
def meeting(request):
    if request.method == 'GET':
        meetings = Meeting.objects.filter(date__mentor=request.user)
        return render(request, 'meeting.html', {'meetings': meetings})
    elif request.method == 'POST':
        date = request.POST.get('date')
        date = datetime.strptime(date, '%Y-%m-%dT%H:%M')

        availability = AppointmentAvailability.objects.filter(mentor=request.user).filter(appointment_date__gte=date - timedelta(minutes=52), appointment_date__lte=date + timedelta(minutes=52)) 

        if availability.exists():
            messages.add_message(request, constants.ERROR, 'Meeting slot not available')
            return redirect('meeting')

        availability = AppointmentAvailability(
            appointment_date=date,
            mentor=request.user
        )

        availability.save()
        messages.add_message(request, constants.SUCCESS, 'Meeting slot scheduled successfully')
        return redirect('meeting')

def auth(request):
    if request.method == 'GET':
        return render(request, 'auth_mentee.html')
    elif request.method == 'POST':
        token = request.POST.get('token')
        try:
            mentee = Mentorship.objects.get(token=token)
            response = redirect('available_dates')
            response.set_cookie('auth_token', token, max_age=3600 ,httponly=True)
            return response
        except Mentorship.DoesNotExist:
            messages.add_message(request, constants.ERROR, 'Invalid token')
            return redirect('auth_mentee')

@mentee_token_required 
def available_dates(request):
    mentee = request.mentee # Get mentee attached by decorator

    if request.method == 'GET':
        availability_queryset = AppointmentAvailability.objects.filter(
            mentor=mentee.user,
            appointment_date__gte=datetime.now(), 
            scheduled=False
        ).values('id', 'appointment_date')


        key='appointment_date'    
        availability_formatted = []
        unique_dates = set()

        for avail in availability_queryset:
            date_only = avail[key].date()
            if date_only in unique_dates:
                continue
            
            unique_dates.add(date_only)
            month_name = avail[key].strftime('%B')
            weekday = avail[key].strftime('%A')
            
            availability_formatted.append({
                'id': avail['id'],
                'month': month_name,
                'weekday': weekday,
                'appointment_date': avail[key].strftime('%d/%m/%Y')
            })
        
        return render(request, 'available_dates.html', {'availability': availability_formatted})

@mentee_token_required 
def schedule_meeting(request):
    mentee = request.mentee # Get mentee attached by decorator

    if request.method == 'GET':
        date = request.GET.get('date')
        date = date.replace('/', '-')
        date = datetime.strptime(date, '%d-%m-%Y')

        hours = AppointmentAvailability.objects.filter(
            mentor=mentee.user,
            appointment_date__gte=date,
            appointment_date__lt=date + timedelta(days=1),
            scheduled=False
            )       
                     
        return render(request, 'schedule_meeting.html', {'hours': hours, 'tags': Meeting.tag_choices}) 
    elif request.method == 'POST':
        hour_id = request.POST.get('hour')
        tag = request.POST.get('tag')
        description = request.POST.get('description')
        with transaction.atomic():
            availability = AppointmentAvailability.objects.get(id=hour_id)
            
            if availability.mentor != mentee.user:
                messages.add_message(request, constants.ERROR, 'You cannot schedule meetings with this mentor')
                return redirect('available_dates')
            
            meeting = Meeting(
                date=availability,
                tag=tag,
                description=description,
                mentee=mentee
            )

            meeting.save()
            availability.scheduled = True
            availability.save()

        messages.add_message(request, constants.SUCCESS, 'Meeting scheduled successfully')
        return redirect('available_dates')

@mentor_owns_mentee_required 
def task(request , id):
    mentee = request.mentee # Get mentee attached by decorator
    
    if request.method == 'GET':
        tasks = Task.objects.filter(mentee=mentee)
        videos = Upload.objects.filter(mentee=mentee)
        return render(request, 'task.html', { 'mentee': mentee, 'tasks': tasks, 'videos': videos })
    
    elif request.method == 'POST':
        task_description = request.POST.get('task')
        new_task = Task(
            task=task_description,
            mentee=mentee,
        )
        new_task.save()
        messages.add_message(request, constants.SUCCESS, 'Task registered successfully')
        return redirect(f'/mentorship/task/{mentee.id}')

@mentor_owns_mentee_required
def upload(request, id):
    mentee = request.mentee # Get mentee attached by decorator

    video_file = request.FILES.get('video')
    new_upload = Upload(
        video=video_file,
        mentee=mentee
    )
    new_upload.save()
    messages.add_message(request, constants.SUCCESS, 'Video uploaded successfully')        
    return redirect(f'/mentorship/task/{mentee.id}')

@mentee_token_required 
def mentee_tasks(request):
    mentee = request.mentee # Get mentee attached by decorator
    
    if request.method == 'GET':
        tasks = Task.objects.filter(mentee=mentee)
        videos = Upload.objects.filter(mentee=mentee)
        return render(request, 'mentee_tasks.html', { 'mentee': mentee, 'tasks': tasks, 'videos': videos })
    
@csrf_exempt
@task_status_checks_required 
def task_status(request, id):
    task = request.task # Get task attached by decorator
    
    task.done = not task.done
    task.save()
    return HttpResponse('Task status updated successfully')

def mentee_logout(request):
    """Logs out the mentee by deleting the auth token cookie and redirecting."""
    response = redirect('auth_mentee')
    response.delete_cookie('auth_token')
    messages.add_message(request, constants.SUCCESS, 'You have been logged out.')
    return response
