from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User

# NOTE Example:- Custom Authentication

class CustomAuthentication(BaseAuthentication):
    def authenticate(self, request):
        username = request.GET.get('username')
        if username is not None:
            try:
                user = User.objects.get(username = username)
                return (user, None)
            
            except User.DoesNotExist:
                raise AuthenticationFailed('No Such of User')
            
        else:
            return None
        
        raise AuthenticationFailed('Authentication credentials were not provided.')
    




"""
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

class CustomAuthentication(BaseAuthentication):
    def authenticate(self, request):
        Implement your authentication logic here
        You can access request.user and request.auth to set the authenticated user and authentication credentials

        If authentication is successful, return a tuple of (user, auth) or None if authentication fails
        Example: return (user, None)

        If authentication credentials are invalid, raise AuthenticationFailed exception
        Example: raise AuthenticationFailed('Invalid token')

        raise AuthenticationFailed('Authentication credentials were not provided.')

"""