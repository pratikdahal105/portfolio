from django.urls import path
from .views import award_list_create, award_detail

urlpatterns = [
    path('awards/', award_list_create),
    path('awards/<uuid:id>/', award_detail),
]
