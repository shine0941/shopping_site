from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import AdminUser,User, Customer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'is_active']

class BaseUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(help_text="使用者登入用 email")
    password = serializers.CharField(write_only=True, help_text="密碼")
    class Meta:
        model = User
        fields = ['email']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("此 email 已被註冊")
        return value
    
class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'user', 'total_spent', 'birthday', 'membership_level']

class AdminUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = AdminUser
        fields = ['id', 'user', 'role', 'display_name', 'brand_name', 'brand_logo', 'description']
class AdminRegisterSerializer(BaseUserSerializer):
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

class AdminTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        try:
            admin_user = AdminUser.objects.get(user=self.user)
            data['user'] = {
                'id': self.user.id,
                'email': self.user.email,
                'role': admin_user.role,
                'display_name': admin_user.display_name,
            }
        # except AdminUser.DoesNotExist:
        except Exception as e:
            raise serializers.ValidationError('此帳號不是後台使用者')

        return data
    
class CustomerRegisterSerializer(BaseUserSerializer):
    

    class Meta:
        model = User
        fields = ['email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )

        Customer.objects.create(user=user)
        return user

class CustomerTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        try:
            customer_user =  Customer.objects.get(user=self.user)
            data['user'] = {
                'id': self.user.id,
                'email': self.user.email,
                'full_name': customer_user.full_name,
                'birthday': customer_user.birthday,
                'total_spent': customer_user.total_spent,
                'membership_level': customer_user.membership_level,
            }
        # except customer_user.DoesNotExist:
        except Exception as e:
            print(f"error:{e}")
            raise serializers.ValidationError('此帳號不是後台使用者')

        return data