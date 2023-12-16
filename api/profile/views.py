from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(["GET"])
def index(request):
    data = {"status": True, "message": "Testing API", "data": None}
    return Response(data)