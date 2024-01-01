from django.urls import path
from . import views

urlpatterns = [
    path('skills/', views.skill_list_create),
    path('skills/<uuid:id>/', views.skill_detail),
]
