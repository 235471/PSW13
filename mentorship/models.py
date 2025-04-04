from datetime import timedelta
import secrets
from django.db import models
from django.contrib.auth.models import User

class Navigator(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name    
    
# Create your models here.
class Mentorship(models.Model):
    stage_choices = (
        ('E1', '10-100k'),
        ('E2', '100k-200k'),
        ('E3', '200k-300k'),
        ('E4', '300k-400k'),
        ('E5', '400k-500k'),
        ('E6', '500k-600k'),
        ('E7', '600k-700k'),
        ('E8', '700k-800k'),
        ('E9', '800k-1M'),
    )
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='photos', null=True, blank=True)
    stage = models.CharField(max_length=2, choices=stage_choices)
    navigator = models.ForeignKey(Navigator, null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=16)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.unique_token()

        super().save(*args, **kwargs)

    def unique_token(self):         
        while True:
            token = secrets.token_urlsafe(8)
            if not Mentorship.objects.filter(token=token).exists():
                return token            

class AppointmentAvailability(models.Model):
    appointment_date = models.DateTimeField(null=True, blank=True) 
    mentor = models.ForeignKey(User, on_delete=models.CASCADE)
    scheduled = models.BooleanField(default=False)

    def appointment_end_time(self):
        return self.appointment_date + timedelta(minutes=50)
    
    def __str__(self):
        return str(self.appointment_date)
    
class Meeting(models.Model):
    tag_choices = (
    ('D', 'Django'),
    ('F', 'Flask'),
    ('P', 'Basic Python'),
    ('A', 'RESTful APIs'),
    ('B', 'Databases'),
    ('ORM', 'Object-Relational Mapping'),
    ('SQL', 'SQL'),
    ('ML', 'Machine Learning'),
    ('AI', 'Artificial Intelligence'),
    ('TDD', 'Test-Driven Development'),
    ('CS', 'Data Structures & Algorithms'),
    ('P', 'Functional Programming'),
    ('CI/CD', 'Continuous Integration / Continuous Deployment'),
    ('U', 'Usability'),
    ('S', 'Security'),
    ('AIO', 'Async Programming / AsyncIO'),
    ('C', 'Cloud Computing'),
    ('R', 'RPA (Robotic Process Automation)'),
    ('GIT', 'Version Control (Git)'),
    ('T', 'Testing'),
    ('DHT', 'Technical Skills Development')
    )

    date = models.ForeignKey(AppointmentAvailability, on_delete=models.CASCADE)
    mentee = models.ForeignKey(Mentorship, on_delete=models.CASCADE)
    tag = models.CharField(max_length=5, choices=tag_choices)
    description = models.TextField()    

class Task(models.Model):
    mentee = models.ForeignKey(Mentorship, on_delete=models.DO_NOTHING)
    task = models.CharField(max_length=255)
    done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.task

class Upload(models.Model):
    mentee = models.ForeignKey(Mentorship, on_delete=models.DO_NOTHING)
    video = models.FileField(upload_to='videos')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.video.name
