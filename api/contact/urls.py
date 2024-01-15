from django.urls import path
from . import views

urlpatterns = [
    path('contacts/', views.contact_list_create),
    path('contacts/<uuid:id>/', views.contact_detail),
]
