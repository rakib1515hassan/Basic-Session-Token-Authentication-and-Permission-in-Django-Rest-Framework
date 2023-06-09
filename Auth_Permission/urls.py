from django.urls import path, include
# from Auth_Permission.views import StudentModelViewSet, StudentModelDetailViewSet , StudentList, StudentDetail, StudentModelList
from Auth_Permission.views import *
from rest_framework.routers import DefaultRouter



# Creating Router Object
router = DefaultRouter()

# Router Registration StudentViewSet With Router
router.register('studentapi', StudentModelViewSet, basename='student')
router.register('studentapidetails', StudentModelDetailViewSet, basename='studentdetails')


urlpatterns = [
    path('viewsets/', include(router.urls)),
    path('students-model-list/', StudentModelList.as_view(), name='StudentModelList'),
    path('students-model-detail/<int:pk>/', StudentModelDetail.as_view(), name='StudentModelDetail'),

    path('students-list/', StudentList.as_view(), name='StudentList'),
    path('students-detail/<int:pk>/', StudentDetail.as_view(), name='student-detail'),

    path('Student_Info/', Student_Info),
    path('Student_Info/<int:pk>/', Student_Info),


    # For Session Authentication Weneed Login Form, That whay it are needed.
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
]
