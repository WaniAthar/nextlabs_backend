from django.conf import settings
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf.urls.static import static
from main.views import (
    AdminLoginView,
    AllTasksView,
    AppView,
    CheckPermissionView,
    CreateAppCategoryView,
    CreateAppSubCategoryView,
    CreateAppView,
    CreateTaskView,
    GetCategoryView,
    GetPointsView,
    SignupView,
    UserView,
)


urlpatterns = [
    path("api/token", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/admin/login/", AdminLoginView.as_view(), name="admin_login"),
    path("api/token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/app/", AppView.as_view(), name="app"),
    path("api/signup/", SignupView.as_view(), name="signup"),
    path("api/user/", UserView.as_view(), name="user"),
    path("api/app/create/", CreateAppView.as_view(), name="create_app"),
    path("api/category/", GetCategoryView.as_view(), name="get_category"),
    path(
        "api/category/create/", CreateAppCategoryView.as_view(), name="create_category"
    ),
    path(
        "api/subcategory/create/",
        CreateAppSubCategoryView.as_view(),
        name="create_subcategory",
    ),
    path("api/task/all/", AllTasksView.as_view(), name="all_tasks"),
    path("api/points/", GetPointsView.as_view(), name="get_points"),
    path("api/task/create/", CreateTaskView.as_view(), name="create_task"),
    path("api/check_permission/", CheckPermissionView.as_view(), name="check_permission"),
]

# media url
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)