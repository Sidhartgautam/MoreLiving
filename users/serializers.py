from rest_framework import serializers
from django.contrib.auth import get_user_model
from roles.models import Role
from django.contrib.auth import authenticate

User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name'
                  )

    def create(self, validated_data):
        role = Role.objects.get(codename='owner')
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.user_role = role
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def validate(self, data):
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": ("Email already exists")})
        return super().validate(data)
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError({"username": ("Username already exists")})
        return value
    
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate (self, data):
        username = data.get("username", "")
        password = data.get("password", "")

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    msg = ("User account is disabled.")
                    raise serializers.ValidationError(msg)
            else:
                msg = ("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg)
        else:
            msg = ("Must include " "username and password.")
            raise serializers.ValidationError(msg)

        data["user"] = user
        return data
    

