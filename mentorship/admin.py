from django.contrib import admin
from .models import Meeting, Mentorship, Navigator, AppointmentAvailability
# Register your models here.
admin.site.register(Mentorship)
admin.site.register(Navigator)
admin.site.register(AppointmentAvailability)
admin.site.register(Meeting)