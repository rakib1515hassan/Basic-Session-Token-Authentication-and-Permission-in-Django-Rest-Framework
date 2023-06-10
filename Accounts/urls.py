from django.urls import path
from Accounts.views import (
    UserRegistrationView, 
    UserLoginView, 
    UserProfileView,
)
# from rest_framework_simplejwt.views import TokenRefreshView

from Accounts.views import *

# authtoken Create
from rest_framework.authtoken.views import obtain_auth_token
from Accounts.auth import CustomAuthToken
# Creating Router Object

urlpatterns = [
    # NOTE Deffult Django Token Create URL = ( http://127.0.0.1:8000/account/api-token-auth/ )
    ## To hit this url (http POST http://127.0.0.1:8000/account/api-token-auth/ username="admin" password="admin")
    # path('api-token-auth/', obtain_auth_token)

    # NOTE Custom Token Create URL = ( http://127.0.0.1:8000/account/custom_authtoken_genarate/ )
    ## To hit this url ( http POST http://127.0.0.1:8000/account/custom_authtoken_genarate/ username="admin" password="admin" )
    path('custom_authtoken_genarate/', CustomAuthToken.as_view(), name='CustomAuthToken'),

    path('register/', UserRegistrationView.as_view(), name='UserRegistrationView'),
    path('login/', UserLoginView.as_view(), name='UserLoginView'),
    path('user-profile/', UserProfileView.as_view(), name='UserProfileView'),
    

]
