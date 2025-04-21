# myapp/urls.py

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
   path('', views.index, name='index'),
   #  path('verify-otp/', views.verify_otp, name='verify_otp'),
   #  path('submit/', views.submit_application, name='submit_application'),
    path('guidelines/', views.guidelines, name='guidelines'),
    path('timeline/', views.timeline, name='timeline'),
    path('apply/<int:problem_id>/', views.apply_problem_view, name='apply_problem'),
    path('send-otp/', views.send_otp_view, name='send_otp'),
    path('export-students/', views.export_students_excel, name='export_students_excel'),

   

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
