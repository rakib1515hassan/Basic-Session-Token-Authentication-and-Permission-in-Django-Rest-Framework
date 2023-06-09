from django.urls import path
from Accounts.views import UserRegistrationView, UserLoginView
# from rest_framework_simplejwt.views import TokenRefreshView

from Accounts.views import *

# authtoken Create
from rest_framework.authtoken.views import obtain_auth_token
from Accounts.auth import CustomAuthToken
# Creating Router Object

urlpatterns = [
    # authtoken Create
    # To hit this url (http POST http://127.0.0.1:8000/authtoken_genarate/ username="your_username" password="your_password")
    # path('authtoken_genarate/', obtain_auth_token),
    path('custom_authtoken_genarate/', CustomAuthToken.as_view()),

    path('register/', UserRegistrationView.as_view(), name='UserRegistrationView'),
    path('login/', UserLoginView.as_view(), name='UserLoginView'),
    # path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    

    

]
