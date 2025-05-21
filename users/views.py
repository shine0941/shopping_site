from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import AdminRegisterSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

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

class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, email=email, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            })
        return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
