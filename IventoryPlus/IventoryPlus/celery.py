from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# تعيين متغير البيئة للملف الإعدادات الخاص بـ Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'IventoryPlus.settings')

# إنشاء تطبيق Celery
app = Celery('IventoryPlus')

# تعيين وسيط الرسائل وقاعدة بيانات النتائج (اختياري، إذا كنت تستخدم Redis)
app.conf.broker_url = 'redis://localhost:6379/0'
app.conf.result_backend = 'redis://localhost:6379/0'

# تحميل إعدادات Celery من ملف الإعدادات الخاص بـ Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# اكتشاف المهام بشكل تلقائي
app.autodiscover_tasks()

# تعريف اسم التطبيق الذي سيتم تصديره
__all__ = ('app',)
