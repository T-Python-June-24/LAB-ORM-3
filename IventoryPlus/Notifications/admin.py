from django.contrib import admin
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from celery.schedules import crontab
# Register your models here.

def create_periodic_task():
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=1,
        period=IntervalSchedule.HOURS
    )
    
    PeriodicTask.objects.create(
        interval=schedule,
        name='Check Quantity and Date',
        task='Notifications.tasks.check_quantity_and_date',
    )

