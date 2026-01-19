from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Teacher 

class TeacherListView(APIView):
    def get(self, request):
        teachers = Teacher.objects.all()
        data=[]
        for x in teachers:
            print(x.name)
            data.append({
                'name': x.name,
                'email': x.email,
                'phone': x.phone,
                "department": x.department,
            })
        
        return Response(data)
