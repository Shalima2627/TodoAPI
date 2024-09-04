from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,permissions
from .models import Todo
from .serializers import TodoSerializer

#In this TodoAPI it class-based
class TodoListAPIView(APIView):
    #Add Permission to check if the user is autheticated
    permission_classes = [permissions.IsAuthenticated]
    
    #For listing all tasks
    def get(self,request,*args,**kwargs):
        qs = Todo.objects.all()
        todos = Todo.objects.filter(user = request.user.id)
        serializer = TodoSerializer(todos, many = True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    #For creating a Task
    def post(self,request,*args,**kwargs):
        data = {
            'task' : request.data.get('task'),
            'completed' : request.data.get('completed'),
            'user' : request.user.id
        }
        serializer = TodoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)
    
    
class DetailTodoAPIView(APIView):
    #Add Permission to check if the user is autheticated
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self, todo_id,user_id):
        try:
            return Todo.objects.get(id=todo_id,user=user_id)
        except Todo.DoesNotExist:
            return None
    
    #Retrive the task for a userid
    def get(self,request,todo_id,*args, **kwargs):
        todo_instance = self.get_object(todo_id,request.user.id)
        if not todo_instance:
            return Response(
                {"res":"Object with todo id does not exist"},
                status = status.HTTP_400_BAD_REQUEST
            )
        serializer = TodoSerializer(todo_instance)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    #For Updating the task
    def put(self,request,todo_id,*args ,**kwargs):
        todo_instance = self.get.object(todo_id,request.user.id) 
        if not todo_instance:
            return Response(
                {"res":"Object with todo id does not exist"},
                status = status.HTTP_400_BAD_REQUEST
            )
        data = {
            'task' : request.data.get('task'),
            'completed' : request.data.get('completed'),
            'user' : request.user.id
        }
        serializer = TodoSerializer(instance = todo_instance,data=data,partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #For deleting a task
    def delete(self,request,todo_id,*args,**kwargs):
        todo_instance = self.get_object(todo_id,request.user.id)
        if not todo_instance:
            return Response(
                {"res":"Object with todo id does not exist"},
                status = status.HTTP_400_BAD_REQUEST
            )
        todo_instance.delete()
        return Response(
            {'res' : 'Object Deleted'},
            status = status.HTTP_200_OK
        )