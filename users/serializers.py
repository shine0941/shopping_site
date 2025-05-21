from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import AdminUser

User = get_user_model()

class AdminRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(help_text="使用者登入用 email")
    password = serializers.CharField(write_only=True, help_text="密碼")
    role = serializers.ChoiceField(choices=AdminUser.ROLE_CHOICES, help_text="角色類型（merchant 或 manager）")
    display_name = serializers.CharField()
    brand_name = serializers.CharField(required=False, allow_blank=True)
    brand_logo = serializers.ImageField(required=False, allow_null=True)
    description = serializers.CharField(required=False, allow_blank=True)
    

    class Meta:
        model = User
        fields = ['email', 'password', 'role', 'display_name', 'brand_name', 'brand_logo', 'description']

    def create(self, validated_data):
        role = validated_data.pop('role')
        display_name = validated_data.pop('display_name')
        brand_name = validated_data.pop('brand_name', '')
        brand_logo = validated_data.pop('brand_logo', None)
        description = validated_data.pop('description', '')

        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )

        AdminUser.objects.create(
            user=user,
            role=role,
            display_name=display_name,
            brand_name=brand_name,
            brand_logo=brand_logo,
            description=description
        )
        return user
