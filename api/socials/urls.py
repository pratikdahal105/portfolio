from django.urls import path
from . import views

urlpatterns = [
    path('socials/', views.socials_list_create),
    path('socials/<uuid:id>/', views.socials_detail),
]
