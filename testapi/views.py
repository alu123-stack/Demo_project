from rest_framework.views import APIView
from rest_framework.response import Response
from testingapp.models import *
from testingapp.serializers import *
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class TaskListApiView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        task = Task.objects.filter(user=request.user)
        serializer = TaskSerializer(task,many=True)
        response_data = {
            'resp_code': 1,
            'data': serializer.data,
            'message':'success',
        } 
        return Response(response_data)

class TaskCreateApiView(APIView):
    def post(self,request):
        data = request.data
        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                'resp_code':1,
                'data':serializer.data,
                'messsage':"task created"
            }
        else:
            response_data = {
                'resp_code':0,
                'messsage':serializer.errors,

            }
        return Response(response_data)


