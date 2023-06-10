from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from Accounts.models import Profile


# -----------------------------( For Token )-----------------------------------------
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

#     @classmethod
#     def get_token(cls, user):
#         token = super(MyTokenObtainPairSerializer, cls).get_token(user)

#         # Add custom claims
#         token['username'] = user.username
#         return token

# ---------------------------( For Registrations )------------------------------------
class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password], style={'input_type':'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type':'password'})

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'password':{'write_only':True}
        }
    # Validating Password and Confirm Password while Registration
    def validate(self, attrs): # attrs means data
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        return attrs
    # NOTE An alternative way for password validation
    """
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        return attrs
    """

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
   
        user.set_password(validated_data['password'])
        user.save()

        return user
    

# --------------------------------( For Login )----------------------------------------
class UserLoginSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(max_length=255)
#   username = serializers.CharField(max_length=255)
  class Meta:
    model = User
    fields = ['email', 'password']
    # fields = ['username', 'password']




# --------------------------------( User Profile )----------------------------------------
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email',]




# NOTE -------------( Alter Native way )-------------------------
# class AlbumSerializer(serializers.ModelSerializer):
#     tracks = serializers.SlugRelatedField(
#         many=True,
#         read_only=True,
#         slug_field='title'
#      )

#     class Meta:
#         model = Album
#         fields = ['album_name', 'artist', 'tracks']