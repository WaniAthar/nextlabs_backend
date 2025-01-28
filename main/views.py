from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from .models import App, Category, SubCategory, Task
from .serializers import (
    AdminLoginSerializer,
    AppSerializer,
    CategorySerializer,
    PointsSerializer,
    SubCategorySerializer,
    TaskSerializer,
    UserSerializer,
)
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework import status
from rest_framework.response import Response
import json
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


# Create your views here.
class AppView(generics.ListCreateAPIView):
    queryset = App.objects.all()
    serializer_class = AppSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = App.objects.exclude(task__user = self.request.user)
        return queryset


class SignupView(generics.CreateAPIView):
    """
    API endpoint for user registration with token return.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        # Save the user using the serializer
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Generate tokens for the user
            refresh = RefreshToken.for_user(user)

            # Return the response with tokens
            return Response(
                {
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "name": user.name,
                    },
                    "tokens": {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# update user
class UserView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Override this method to retrieve the current user.
        """
        return self.request.user

    def delete(self, request, *args, **kwargs):
        """
        Customize delete to handle user deactivation instead of hard delete.
        """
        user = self.get_object()
        user.is_active = False  # Deactivate user instead of hard delete
        user.save()
        return Response({"message": "User account has been deactivated."}, status=204)


class CreateAppView(generics.CreateAPIView):
    queryset = App.objects.all()
    serializer_class = AppSerializer
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        print(request.data)
        return super().post(request, *args, **kwargs)


class CreateAppCategoryView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class CreateAppSubCategoryView(generics.CreateAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class AllTasksView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.get_object())
        return queryset


class GetPointsView(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = PointsSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.get_object())
        return queryset


class GetCategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]



class CreateTaskView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        print(request.data)
        return super().post(request, *args, **kwargs)


class AdminLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = AdminLoginSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer.validated_data)
            try:
                user = User.objects.get(email=request.data["email"])
            except User.DoesNotExist:
                return Response(
                    {"message": "Invalid credentials"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            if user.check_password(request.data["password"]) and user.is_superuser:
                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        "access":str(refresh.access_token),
                        "refresh":str(refresh)
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"message": "You are not authorized to access this resource"},
                    status=status.HTTP_403_FORBIDDEN,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckPermissionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return Response({
                "is_superuser": True,
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "is_superuser": False,
            }, status=status.HTTP_200_OK)