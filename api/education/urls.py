from django.urls import path
from . import views

urlpatterns = [
    path('educations/', views.education_list_create),
    path('educations/<uuid:id>/', views.education_detail),
]
