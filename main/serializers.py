import base64
from rest_framework import serializers
from .models import App, Category, SubCategory, Task
from django.contrib.auth import get_user_model
from django.db import models
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

User = get_user_model()


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ["id", "name"]
        read_only_fields = ["id"]


class CategorySerializer(serializers.ModelSerializer):
    subcategory = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ["id", "name", "subcategory"]
        read_only_fields = ["id", "subcategory"]


class AppSerializer(serializers.ModelSerializer):
    appCategory = CategorySerializer(read_only=True)
    appSubCategory = SubCategorySerializer(read_only=True)

    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),source="appCategory", write_only=True
    )
    subcategory = serializers.PrimaryKeyRelatedField(
        queryset=SubCategory.objects.all(), source="appSubCategory", write_only=True
    )

    class Meta:
        model = App
        fields = ["id", "name", "app_link", "points", "image", "appCategory", "appSubCategory", "category", "subcategory"]




class TaskSerializer(serializers.ModelSerializer):
    app = AppSerializer(read_only=True)
    app_id = serializers.PrimaryKeyRelatedField(
        queryset=App.objects.all(), source="app", write_only=True
    )
    class Meta:
        model = Task
        fields = ["id", "user", "app" , "screen_shot","app_id"]
        read_only_fields = ["id"]
    

class PointsSerializer(serializers.ModelSerializer):
    total_points = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ["total_points"]

    def get_total_points(self, obj):
        total_points = (
            Task.objects.filter(user=self.context["request"].user).aggregate(
                total_points=models.Sum("app__points")
            )["total_points"]
            or 0
        )
        return total_points


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        """
        Create a new user instance.
        """
        password = validated_data.pop("password", None)
        user = User(**validated_data)
        if password:
            user.set_password(password)  # Hash the password
        user.save()
        return user
    


class AdminLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        user = User.objects.get(email=email)
        if not user.check_password(password):
            raise serializers.ValidationError("Invalid email or password")
        if not user.is_superuser:
            raise serializers.ValidationError("User is not an admin")
        return user
    

