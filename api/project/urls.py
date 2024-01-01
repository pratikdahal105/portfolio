from django.urls import path
from . import views

urlpatterns = [
    path('projects/', views.project_list_create),
    path('projects/<uuid:id>/', views.project_detail),
]
