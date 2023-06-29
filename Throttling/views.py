from django.shortcuts import render
from Auth_Permission.models import Student
from Auth_Permission.serializers import StudentSerializer
from rest_framework.response import Response
from rest_framework import status
# Function Based
from rest_framework.decorators import api_view, authentication_classes, permission_classes, throttle_classes
# Class Based
from rest_framework.views import APIView

from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    ListCreateAPIView,
)

# For Authentication --------------------------
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from Auth_Permission.custom_authentication import CustomAuthentication
from rest_framework.permissions import (
    IsAdminUser, 
    IsAuthenticated, 
    IsAuthenticatedOrReadOnly, 
    AllowAny, 
    DjangoModelPermissions, 
    DjangoModelPermissionsOrAnonReadOnly, 
    DjangoObjectPermissions
)

from Auth_Permission.permissions import Only_GET_allow, IsSuperUser # Custom permissions

# Throttling এর মাধ্যমে আমরা Api request hendel কোরতে পারবো, একজন authenticate and unauthenticate user একটি নির্দিস্ট 
# সময় কতগুলো request কোরতে পারবে তা আমরা assign করে দিতে পারবো।
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle, ScopedRateThrottle
from Throttling.throttling import Custom_1, Custom_2, Custom_3


# Create your views here.
class Student_Throttling(ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    # NOTE -----Authentication------------
    authentication_classes = [SessionAuthentication]

    # NOTE -----Permission----------------
    permission_classes = [IsAuthenticatedOrReadOnly]

    # NOTE -----Throttling----------------
    # throttle_classes = [AnonRateThrottle, UserRateThrottle] # set time in setting.py unknown user = 2/day and user = 5/day
    throttle_classes = [AnonRateThrottle, Custom_1] 



""" NOTE For Function View:-

    @api_view(['GET'])
    @throttle_classes([UserRateThrottle])
    def example_view(request, format=None):
        content = {
            'status': 'request was permitted'
        }
        return Response(content)
    
    NOTE: It's also possible to set throttle classes for routes that are created using the @action decorator. Throttle classes set in this way will override any viewset level class settings.

    @action(detail=True, methods=["post"], throttle_classes=[UserRateThrottle])
    def example_adhoc_method(request, pk=None):
        content = {
            'status': 'request was permitted'
        }
        return Response(content)

"""


class ContentListView(ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'Content'  # '5/minute',


class ContentCreateView(CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'modyfy'  # '2/day',


class ContentRetrieveView(RetrieveAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'Content'  # '5/minute',


class ContentUpdateView(UpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'modyfy'  # '2/day',
    