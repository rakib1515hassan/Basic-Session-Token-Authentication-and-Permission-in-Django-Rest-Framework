from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db.models import Q

from Accounts.serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
)

from Accounts.auth import CustomAuthToken

from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

# Authentication and Parmission
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    AllowAny,
    DjangoModelPermissions,
    DjangoModelPermissions,
    DjangoObjectPermissions,
)



## Create your views here.-----------------------------------------------------------------------------------
class UserRegistrationView(APIView):
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = CustomAuthToken()
            # Call the post method to generate and save the token
            response = token.post(request)
            # Get the token value from the response
            token_value = response.data.get('token')
            # Return the response with the token and message
            return Response({'token': token_value, 'msg': 'Registration Successful'}, status=status.HTTP_201_CREATED)

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
            username = usr.username
            # password_status = usr.check_password(password)
            
            # Authenticate the user
            user = authenticate(username=username, password=password)
            
            if user is not None:
                ## NOTE Token Genarate-----------------------------------
                # Generate or retrieve the token for the user
                token, created = Token.objects.get_or_create(user=user)

                # Return the response with the token and message
                return Response({'token': token.key, 'msg': 'Login Success'}, status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)
            
        except User.DoesNotExist:
            return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# NOTE যদি username, password এর মাধ্যমে আমরা Login কোরতে চাই তবে এই ভাবে করতে হবে।

# class UserLoginView(APIView):
#     def post(self, request, format=None):
#         serializer = UserLoginSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             username = serializer.data.get('username')
#             password = serializer.data.get('password')

#             user = authenticate(username= username , password=password)            

#             if user is not None:
#                 ## NOTE Token Genarate-----------------------------------
#                 token = CustomAuthToken()
#                 # Call the post method to generate and save the token
#                 response = token.post(request)
#                 # Get the token value from the response
#                 token_value = response.data.get('token')
#                 # Return the response with the token and message          
#                 return Response({'token': token_value,'msg':'Login Success'}, status=status.HTTP_200_OK)
#             else:
#                 return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)
                        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





# URL = ( http://127.0.0.1:8000/account/user-profile/ )
class UserProfileView(APIView):
    # authentication_classes = [BasicAuthentication]
    # authentication_classes = [SessionAuthentication]
    # authentication_classes = [BasicAuthentication, SessionAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
