from rest_framework import serializers
from django.contrib.auth.models import User

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    staff_status = 1
    class Meta:
        model = User
        fields = ["id","username", "email", "password"]
        
        
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email"),
            password=validated_data["password"],
        )
        user.is_staff = True  # set staff status
        user.save()
        return user
