from rest_framework.permissions import BasePermission
from datetime import datetime, timedelta

from django.utils import timezone
from rest_framework import permissions


# If User is is_superuser then he can access this api else not access
class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser
    



# এটি একটি customparmission create করা হয়েছে, এখানে বলা হয়েছে যদি কোন user only GET method এর জন্যে request 
# করে তবে তা allow , but POST, PUT, DELERE method এর জন্যে তা allow না।
class Only_GET_allow(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return False
    


class AuthorAllStaffAllButEditOrReadOnly(permissions.BasePermission):
    edit_methods = ("PUT", "PATCH")
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.author == request.user:
            return True

        if request.user.is_staff and request.method not in self.edit_methods:
            return True

        return False
    





# Let's say you want to restrict access to objects older than 10 minutes for everyone except superusers:
class ExpiredObjectSuperuserOnly(permissions.BasePermission):
    message = "This object is expired." # custom error message
    def object_expired(self, obj):
        expired_on = timezone.make_aware(datetime.now() - timedelta(minutes=10))
        return obj.created < expired_on

    def has_object_permission(self, request, view, obj):

        if self.object_expired(obj) and not request.user.is_superuser:
            return False
        else:
            return True
"""
    In this permission class, the has_permission method is not overridden -- so it will always return True.

    Since the only important property is the object's creation time, the check happens in has_object_permission (since we don't have access to an object's properties in has_permission).

    So, if a user wants to access the expired object, the exception PermissionDenied is raised:
"""


class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return False
    



class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if obj.author == request.user:
            return True
        return False
    


class IsFinancesMember(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name="Finances").exists():
            return True