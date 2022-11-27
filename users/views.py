from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, response, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters import rest_framework as filters

from users.serializers import (
    UserSerializer,
    LogoutSerializer,
    ProfileSerializer,
    UnitsSerializer,
    ApprovedSerializer,
    RegisteredStudentsSerializer,
)
from users.models import Profile, Units, RegisteredStudents, Approved
from users.permissions import IsUser

User = get_user_model()


class UserRegister(APIView):
    def post(self, request: Request, format: str = "json") -> Response:
        serializer = UserSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        response = serializer.data
        response["refresh"] = str(refresh)
        response["access"] = str(refresh.access_token)

        return Response(response, status=status.HTTP_201_CREATED)


class UserView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    queryset = User.objects.all()


class LogoutView(GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request):  # type:ignore[no-untyped-def]

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [
        IsAuthenticated,
        IsUser,
    ]
    serializer_class = ProfileSerializer
    lookup_field = "user"
    queryset = Profile.objects.all()


class ProfileListView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [
        IsAuthenticated,
    ]


class UnitsListCreateView(generics.ListCreateAPIView):
    serializer_class = UnitsSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    queryset = Units.objects.all()


class UnitsDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UnitsSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    queryset = Units.objects.all()
    lookup_field = "id"


class RegisteredStudentsListCreateView(generics.ListCreateAPIView):
    serializer_class = RegisteredStudentsSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    queryset = RegisteredStudents.objects.all()


class RegisteredStudentList(generics.ListCreateAPIView):
    """
    View to only show the students registered to take the unit
    taught by the logged in lecturer
    """

    serializer_class = RegisteredStudentsSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self):
        user = self.request.user
        return RegisteredStudents.objects.filter(unit__lecturer=user)


class RegisteredStudentsDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RegisteredStudentsSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    queryset = RegisteredStudents.objects.all()
    lookup_field = "id"


class ApprovedListCreateView(generics.ListCreateAPIView):
    serializer_class = ApprovedSerializer
    queryset = Approved.objects.all()
    permission_classes = [
        IsAuthenticated,
    ]


class ApprovedDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ApprovedSerializer
    queryset = Approved.objects.all()
    permission_classes = [
        IsAuthenticated,
    ]
    lookup_field = "id"


class MyUnitsView(generics.ListAPIView):
    serializer_class = UnitsSerializer

    def get_queryset(self):
        """
        View to list all units for currently authenticated user
        """
        user = self.request.user
        return Units.objects.filter(lecturer=user)


class MyUnitsStudentsApproveView(generics.ListAPIView):
    """
    View to only display the students marked for the unit that the lecturer
    teaches
    """
    serializer_class = ApprovedSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self):
        user = self.request.user
        return Approved.objects.filter(unit__lecturer=user)


# class UnitStudent(generics.ListAPIView):
#     queryset = RegisteredStudents.objects.all()
#     serializer_class = RegisteredStudentsSerializer
#     filter_backends = (filters.DjangoFilterBackend,)
#     filterset_fields = ('unit',)

# class ApproveUnitStudentView(generics.ListAPIView):
#     queryset = Approved.objects.all()
#     serializer_class = ApprovedSerializer
#     filter_backends = (filters.DjangoFilterBackend,)
#     filterset_fields = ('student',)

# class UnitAndStudentView(generics.ListAPIView):
#     serializer_class = RegisteredStudentsSerializer
#     queryset = RegisteredStudents.objects.all()
#     permission_classes = [IsAuthenticated,]
#     unit_separator = ","

#     def get_queryset(self):
#         units = self.request.query_params.get("unit", None)
#         if units:
#             qs = RegisteredStudents.objects.filter()
#             for unit in units.split(self.unit_separator):
#                 qs = qs.filter(unit=unit)
#             return qs
#         return super().get_queryset()
