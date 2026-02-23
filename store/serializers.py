from rest_framework import serializers
from .models import Category, Product

# =========================
# Product Serializer
# =========================
class ProductSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)  # ✅ ensure URL returned
    description = serializers.CharField(required=False, allow_blank=True)  # ✅ Optional
    class Meta:
        model = Product
        fields = ['id', 'name', 'image', 'price', 'category', 'description']

# =========================
# Category Serializer
# =========================
class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    image = serializers.ImageField(use_url=True)  # <-- Add this line

    class Meta:
        model = Category
        fields = ['id', 'name', 'image', 'products']


# =========================
# Password Reset Serializer (Request)
# =========================
class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        # Optional: check if user exists, but do not reveal for security
        return value

# =========================
# Password Reset Confirm Serializer
# =========================
class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=8)

    def validate_new_password(self, value):
        # Optional: Add extra password validation if desired
        return value
