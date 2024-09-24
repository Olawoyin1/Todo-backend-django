from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import APIView
from rest_framework.response import Response
from .serializer import TodoSerializer
from rest_framework import status
from .models import Todo

# Create your views here.
class TodoList(APIView):
    serializer_class = TodoSerializer
    
    def get(self, request, *args, **kwargs):
        todos=Todo.objects.all()
        serializer =  self.serializer_class(todos, many=True)
        response = {
            "message" : "Todos",
            "data" : serializer.data
        }
        
        return Response(data=response, status=status.HTTP_200_OK)


    def post(self, request, *args, **kwargs):
        data=request.data
        serializer=self.serializer_class(data=data)
        
        
        if serializer.is_valid():
            response = {
                "message": "Successfully Added To The List ",
                "data": serializer.validated_data,
            }
            serializer.save()
            return Response(data=response, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class TodoActions(APIView):
    serializer_class = TodoSerializer
    
    def get(self, request, pk, *args, **kwargs):
        todo=Todo.objects.get(id=pk)
        serializer = self.serializer_class(todo)
        response = {
            "message" : "Todo",
            "data" : serializer.data
        }
        
        return Response(data=response, status=status.HTTP_200_OK)
    
    def put (self, request, pk, *args, **kwargs):
        todo=Todo.objects.get(id=pk)
        data = request.data
        serializer = self.serializer_class(todo, data=data)
        
        if serializer.is_valid():
        
            response = {
                "message" : "List Updated Sucessfully",
                "data" : serializer.validated_data
            }   

            serializer.save()
            
            return Response(data=response, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def patch(self, request, pk, format=None):
        try:
            # Get the todo item by its primary key (id)
            todo = Todo.objects.get(id=pk)
        except Todo.DoesNotExist:
            return Response({'error': 'Todo not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Partial update - only updating the fields sent in the request
        serializer = TodoSerializer(todo, data=request.data, partial=True)
        
        # Validate and save the changes
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request, pk , *args, **kwargs):
        todo = Todo.objects.get(id=pk)
        serializer = self.serializer_class(todo)
        todo.delete()
        response = {
            "message": "Todo deleted successfully",
            "data" : serializer.data
        }


        return Response(data=response, status=status.HTTP_200_OK)
