from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User

class UserListView(APIView):
    def get(self, request):
        users = User.objects.all()
        data = [{'id': u.id, 'username': u.username, 'email': u.email, 'role': u.role, 'first_name': u.first_name, 'last_name': u.last_name} for u in users]
        return Response(data)
