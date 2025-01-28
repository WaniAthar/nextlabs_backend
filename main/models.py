from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and returns a regular user with the given email and password.
        """
        if not email:
            raise ValueError("The Email field must not be empty.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and returns a superuser with the given email and password.
        """
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


# user model, this is where users are stored
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = "email"
    objects = UserManager()

    def __str__(self):
        return self.email


# Admin can add apps, categories, subcategories
class App(models.Model):
    name = models.CharField(max_length=255)
    app_link = models.URLField(max_length=255)
    points = models.IntegerField(default=0)
    image = models.ImageField(upload_to="images")
    appCategory = models.ForeignKey(
        "Category", on_delete=models.CASCADE, blank=True, null=True
    )
    appSubCategory = models.ForeignKey(
        "SubCategory", on_delete=models.CASCADE, blank=True, null=True
    )


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)


class SubCategory(models.Model):
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, related_name="subcategory"
    )
    name = models.CharField(max_length=255, unique=True)


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="task")
    app = models.ForeignKey(App, on_delete=models.CASCADE)
    screen_shot = models.ImageField(upload_to="images")
