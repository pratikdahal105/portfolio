from django.urls import path
from . import views

urlpatterns = [
    path('works/', views.work_list_create),
    path('works/<uuid:id>/', views.work_detail),
]
