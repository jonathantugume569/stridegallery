from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.views import APIView

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.password_validation import validate_password
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings

from .models import Category, Product
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    PasswordResetSerializer,
    PasswordResetConfirmSerializer
)
from django.views.generic import TemplateView

User = get_user_model()

# =========================
# Password Reset Request API
# =========================
class PasswordResetAPIView(APIView):
    permission_classes = []  # Allow anyone

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        users = User.objects.filter(email=email)

        if users.exists():
            for user in users:
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)

                # Send link to FRONTEND
                reset_link = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"

                subject = "Password Reset Requested"
                message = (
                    f"Hi {user.username},\n\n"
                    f"You requested a password reset.\n\n"
                    f"Click the link below to reset your password:\n"
                    f"{reset_link}\n\n"
                    f"If you didn't request this, you can ignore this email."
                )

                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False
                )

        # Always return success for security
        return Response(
            {"success": True, "message": "If this email exists, a reset link has been sent."},
            status=status.HTTP_200_OK
        )


# =========================
# Password Reset Confirm API
# =========================
class PasswordResetConfirmAPIView(APIView):
    permission_classes = []  # Allow anyone

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uid = serializer.validated_data["uid"]
        token = serializer.validated_data["token"]
        new_password = serializer.validated_data["new_password"]

        try:
            uid_decoded = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=uid_decoded)
        except (User.DoesNotExist, ValueError, TypeError):
            return Response(
                {"error": "Invalid reset link."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not default_token_generator.check_token(user, token):
            return Response(
                {"error": "Reset link is invalid or has expired."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate password strength
        try:
            validate_password(new_password, user)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.save()

        return Response(
            {"success": True, "message": "Password has been reset successfully."},
            status=status.HTTP_200_OK
        )


# =========================
# Category ViewSet
# =========================
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticatedOrReadOnly()]

    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        category = self.get_object()
        products = category.products.all()
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)


# =========================
# Product ViewSet
# =========================
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticatedOrReadOnly()]


class ReactAppView(TemplateView):
    template_name = "index.html"