from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.views import (
    UserRegister,
    LogoutView,
    ProfileListView,
    ProfileDetailView,
    UserView,
    UnitsListCreateView,
    UnitsDetailView,
    RegisteredStudentsDetailView,
    RegisteredStudentsListCreateView,
    ApprovedDetailView,
    ApprovedListCreateView,
    MyUnitsView,
    RegisteredStudentList,
    # UnitStudent,
    # ApproveUnitStudentView,
    # UnitAndStudentView,
)

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", UserRegister.as_view(), name="register"),
    path("profile/<str:user>/", ProfileDetailView.as_view(), name="profile"),
    path("users/", UserView.as_view(), name="users"),
    path("profiles/", ProfileListView.as_view(), name="profiles"),
    path("unit/", UnitsListCreateView.as_view(), name="units-list"),
    path("units/<str:id>/", UnitsDetailView.as_view(), name="units-detail"),
    path("student/", RegisteredStudentsListCreateView.as_view(), name="student-list"),
    path("students/<str:id>/", RegisteredStudentsDetailView.as_view(), name="student-detail"),
    path("approve/", ApprovedListCreateView.as_view(), name="approve-list"),
    path("approved/<str:id>/", ApprovedDetailView.as_view(), name="approve-detail"),
    path("myunits/", MyUnitsView.as_view(), name="my-units"),
    path("myunit/", RegisteredStudentList.as_view(), name="specified-unit"),
    # path("approves/<str:student>/", ApproveUnitStudentView.as_view(), name="approves"),
    # path("units", UnitAndStudentView.as_view(), name="units-students"),
]
