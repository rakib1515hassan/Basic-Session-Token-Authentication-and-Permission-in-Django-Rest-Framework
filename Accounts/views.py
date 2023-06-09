from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from Accounts.serializers import UserRegistrationSerializer, UserLoginSerializer
from Accounts.auth import CustomAuthToken

from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.views import APIView

# from rest_framework_simplejwt.views import TokenObtainPairView
# from .serializers import MyTokenObtainPairSerializer



## Create your views here.-----------------------------------------------------------------------------------

class UserRegistrationView(APIView):
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            # token = CustomAuthToken()   ## Token Genaret
            return Response({'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)
            # return Response({'token': token,'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# NOTE যদি email, password এর মাধ্যমে আমরা Login কোরতে চাই তবে এই ভাবে করতে হবে।
class UserLoginView(APIView):
  def post(self, request, format=None):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        email = serializer.data.get('email')
        password = serializer.data.get('password')
    
        try:
            usr = User.objects.get(email = email)
            if usr:
                authenticate(username= usr.username , password=password)
                token = CustomAuthToken(usr)  # Token Genaret           
                return Response({'token': 'token','msg':'Login Success'}, status=status.HTTP_200_OK)
            
        except User.DoesNotExist:
            return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# NOTE যদি username, password এর মাধ্যমে আমরা Login কোরতে চাই তবে এই ভাবে করতে হবে।
"""
class UserLoginView(APIView):
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.data.get('username')
            password = serializer.data.get('password')

            user = authenticate(username= username , password=password)            

            if user is not None:
                token = CustomAuthToken(user) # Token Genaret
                return Response({'token': 'token','msg':'Login Success'}, status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)
                        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""

