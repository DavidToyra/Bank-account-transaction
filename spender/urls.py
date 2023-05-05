from django.urls import path

from . import views

urlpatterns = [
    path('', views.upload_csv, name='upload'),
    path('spend',views.monthly_totals3, name='spend'),
    
]