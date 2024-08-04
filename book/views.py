from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from .models import *
from book.serializer import *

class SignUp(APIView):
    def post(self,request):
        username=request.data.get('username')
        email=request.data.get('email')
        password=request.data.get('password')
        user=User.objects.create_user(username=username,email=email,password=password)
        serializers=Userserializer(user)
        return Response(serializers.data)
    
class UserLogin(APIView):
    def post(self,request):
        username=request.data.get('username')
        password=request.data.get('password')
        if not username or not password:
            return Response({'username and passsword is required'})
        
        user=authenticate(username=username,password=password)
        refresh=RefreshToken.for_user(user)
        return Response(
            {
                "message":"Authentication Successful",
                "refresh":str(refresh),
                "access":str(refresh.access_token)
            },status=status.HTTP_200_OK
        )
        
class BookListCreateApiView(APIView):
    permission_classes=[IsAuthenticated,]

    def get(self,request):
        book=Book.objects.all()
        serializers=Bookserializer(book,many=True)
        return Response(serializers.data)
    def post(self,request):
        serializers=Bookserializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors)

class BookUpdateDeleteApiView(APIView):
    permission_classes=[IsAuthenticated,]
    def get(self,request,pk):
        book=Book.objects.get(id=pk)
        serializers=Bookserializer(book)
        return Response(serializers.data)

    def put(self,request,pk):
        book=Book.objects.get(id=pk)
        serializers=Bookserializer(book,data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors)
        
    def delete(self,request,pk):
        book=Book.objects.get(id=pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
