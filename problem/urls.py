# myapp/urls.py

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
   path('', views.index, name='index'),
   path('verify-otp/', views.verify_otp, name='verify_otp'),
   path('timeline/', views.timeline, name='timeline'),
   path('guidelines/', views.guidelines, name='guidelines'),
   path('upload/', views.upload_excel, name='upload_excel'),
   

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
