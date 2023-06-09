from django.shortcuts import render
from Auth_Permission.models import Student
from Auth_Permission.serializers import StudentSerializer
from rest_framework.response import Response
from rest_framework import status
# Function Based
from rest_framework.decorators import api_view, authentication_classes, permission_classes
# Class Based
from rest_framework.views import APIView

from rest_framework import viewsets
# from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from rest_framework import mixins
# from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin

from rest_framework import generics
# from rest_framework.generics import GenericAPIView, RetrieveUpdateDestroyAPIView

# For Authentication --------------------------
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny, DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly, DjangoObjectPermissions

from Auth_Permission.permissions import Only_GET_allow, IsSuperUser

from rest_framework.exceptions import AuthenticationFailed

# Create your views here.-----------------------------------------------------------------------------------------------
# class CustomAuthentication(BaseAuthentication):
#     def authenticate(self, request):
#         # Implement your authentication logic here
#         # You can access request.user and request.auth to set the authenticated user and authentication credentials

#         # If authentication is successful, return a tuple of (user, auth) or None if authentication fails
#         # Example: return (user, None)

#         # If authentication credentials are invalid, raise AuthenticationFailed exception
#         # Example: raise AuthenticationFailed('Invalid token')

#         raise AuthenticationFailed('Authentication credentials were not provided.')



# NOTE ----------------------------------------------( viewsets )--------------------------------------------------

## This Class Perform CRUD and it inherits GenericAPIView and
## perform list(), retrieve(), create(), partial_update(), destroy().
## This URL (http://127.0.0.1:8000/viewsets/studentapi/ ) Allow: GET, POST, HEAD, OPTIONS
## if you give a id on the url (http://127.0.0.1:8000/viewsets/studentapi/2/) 
## then it Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
class StudentModelViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    # NOTE -----Authentication------------
    authentication_classes = [BasicAuthentication]
    # authentication_classes = [SessionAuthentication]


    # NOTE -----Permission----------------
    # permission_classes = [IsAuthenticated] # is_active = True থাকা লাগবে
    # permission_classes = [IsAdminUser]   # is_Staff = True থাকা লাগবে
    # permission_classes = [AllowAny]      # Without any authentication যেকেউ access পাবে
    permission_classes = [IsAuthenticated, IsSuperUser]  # Here IsSuperUser is a custom permission
    
    # permission_classes = [IsAuthenticatedOrReadOnly]  # কোন user Authenticate না থাকলে সে GET, HEAD or OPTIONS ব্যেতিত 
                                                      # আন্যকোন action perform কোরতে পারবেনা, But Authenticate হলে 
                                                      # যে কোন action perform কোরতে পারবে।

    # permission_classes = [DjangoModelPermissions] # একটি Django Model Create করার সময় আমরা যে parmission গুলো দেই সেগুলোই
                                                  # parmission দিতে Django Admin pannel এ গিয়ে parmission pannel থেকে দিতে পারি।
    
    # permission_classes = [DjangoModelPermissionsOrAnonReadOnly] # এর মাধ্যমে Unauthenticate user only GET action use কোরতে পারবে,
                                                    # But Authenticate করার পর সে DjangoModelPermissions এর মত parmission পাবে।

    # permission_classes = [DjangoObjectPermissions] # কোন একটি object এর সাপেখে আমরা parmission দিতে পারবো, But এতে কিছু Bug রয়েছে।

    # NOTE Custom Permission-------------------
    # permission_classes = [Only_GET_allow]




## Allow: GET
## If URL (http://127.0.0.1:8000/viewsets/studentapidetails/) Show all data
## IF URL (http://127.0.0.1:8000/viewsets/studentapidetails/1/) Show only thos id data
class StudentModelDetailViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer



## Allow: GET, POST, HEAD, OPTIONS
## URL (http://127.0.0.1:8000/students-model-list/)
## It show all data and also you can create data
class StudentModelList(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer




## Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
## URL (http://127.0.0.1:8000/students-model-detail/1/)
## It only show, edit and delete one student data
class StudentModelDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

# NOTE ------------------------------------------------------( mixins )------------------------------------------

## Allow: GET, POST, HEAD, OPTIONS
## URL (http://127.0.0.1:8000/students-list/)
class StudentList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    


## Allow: GET, PUT, DELETE, HEAD, OPTIONS
# ## URL (http://127.0.0.1:8000/students-detail/1/)   
class StudentDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    



# NOTE ----------------------------------------------( Function Based View )-----------------------------------------------
@api_view(['GET', 'POST', 'PUT','PATCH', 'DELETE'])
# @api_view(['GET', 'POST'])
# @api_view(['GET', 'PUT','PATCH', 'DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def Student_Info(request, pk = None):    
    if request.method == 'GET':
        id = pk
        if id is not None:
            std = Student.objects.get(id = id)
            serializer = StudentSerializer(std)
        else:
            std_objs = Student.objects.all()
            serializer = StudentSerializer(std_objs, many=True)
        return Response(serializer.data)
    

    elif request.method == 'POST':
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        id = pk
        if id is not None:
            std = Student.objects.get(id = id)
            serializer = StudentSerializer(std, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PATCH':
        id = pk
        if id is not None:
            std = Student.objects.get(id = id)
            serializer = StudentSerializer(std, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        id = pk
        if id is not None:
            std = Student.objects.get(id = id)
            std.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    

# @api_view(['GET', 'POST', 'PUT','PATCH', 'DELETE'])
# # @api_view(['GET', 'POST'])
# # @api_view(['GET', 'PUT','PATCH', 'DELETE'])
# def Student_Info(request, pk = None):
#     try:
#         std_obj = Student.objects.get(pk=pk)
#         if request.method == 'GET':
#             serializer = StudentSerializer(std_obj)
#             return Response(serializer.data)

#         elif request.method == 'PUT':
#             serializer = StudentSerializer(std_obj, data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#         elif request.method == 'PATCH':
#             serializer = StudentSerializer(std_obj, data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         elif request.method == 'DELETE':
#             std_obj.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#     except Student.DoesNotExist:
#         if request.method == 'GET':
#             std_objs = Student.objects.all()
#             serializer = StudentSerializer(std_objs, many=True)
#             return Response(serializer.data)

#         elif request.method == 'POST':
#             serializer = StudentSerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#         return Response(status=status.HTTP_404_NOT_FOUND)