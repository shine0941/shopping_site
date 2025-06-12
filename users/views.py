# from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics,permissions, viewsets

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.forms.models import model_to_dict
from .models import Customer
from .serializers import AdminRegisterSerializer,AdminTokenObtainPairSerializer,CustomerTokenObtainPairSerializer,CustomerRegisterSerializer,CustomerSerializer

class AdminRegisterView(APIView):

    @extend_schema(
        tags=["Auth / 管理員註冊與登入"],
        request=AdminRegisterSerializer,
        responses={
            201: OpenApiResponse(description="成功註冊"),
            400: OpenApiResponse(description="資料錯誤"),
        },
        examples=[
            OpenApiExample(
                "商家註冊範例",
                value={
                    "email": "merchant@example.com",
                    "password": "12345678",
                    "role": "merchant",
                    "display_name": "咖啡商家",
                    "brand_name": "CoffeeHouse",
                    "description": "我們提供有靈魂的咖啡"
                },
                request_only=True
            )
        ],
        summary="管理員或商家註冊",
        description="建立新的後台使用者（網站管理員或商家），會自動建立對應的 User 與 AdminUser 模型。",
    )

    def post(self, request):
        serializer = AdminRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "Admin user registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminTokenObtainPairView(TokenObtainPairView):
    serializer_class = AdminTokenObtainPairSerializer

class CustomerRegisterView(APIView):

    @extend_schema(
        tags=["Auth / 顧客註冊"],
        request=CustomerRegisterSerializer,
        responses={
            201: OpenApiResponse(description="成功註冊"),
            400: OpenApiResponse(description="資料錯誤"),
        },
        examples=[
            OpenApiExample(
                "顧客註冊範例",
                value={
                    "email": "customer0001@example.com",
                    "password": "12345678",
                },
                request_only=True
            )
        ],
        summary="顧客註冊",
        description="建立新的前台使用者（顧客），會自動建立對應的 User 與 Customer 模型。",
    )

    def post(self, request):
        serializer = CustomerRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "Customer user registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomerTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomerTokenObtainPairSerializer

class CustomerView(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Customer.objects.all()
        return Customer.objects.none()