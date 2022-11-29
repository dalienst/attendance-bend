from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import (
    UniqueValidator,
    UniqueTogetherValidator,
    UniqueForDateValidator,
)
from users.models import Profile, Units, RegisteredStudents, RegisterUnits, MarkStudents
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from django.db.models import Count
from users.validators import (
    validate_password_digit,
    validate_password_lowercase,
    validate_password_symbol,
    validate_password_uppercase,
)

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer of the user model
    User is able to create an account
    An instance of Profile is created once the user registers
    """

    id = serializers.CharField(
        read_only=True,
    )

    username = serializers.CharField(
        max_length=20,
        min_length=4,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    name = serializers.CharField(
        max_length=50,
        min_length=4,
        required=True,
    )

    password = serializers.CharField(
        max_length=128,
        min_length=5,
        write_only=True,
        validators=[
            validate_password_digit,
            validate_password_uppercase,
            validate_password_symbol,
            validate_password_lowercase,
        ],
    )

    class Meta:
        model = User
        fields = ("id", "email", "username", "name", "password")

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.save()
        Profile.objects.create(user=user)
        return user


class ProfileSerializer(serializers.ModelSerializer):
    """
    The profile serializer to enable retrieval and updating of profile of the user
    """

    name = serializers.CharField(read_only=True, source="user.name")
    bio = serializers.CharField(allow_blank=True, required=False)
    location = serializers.CharField(allow_blank=True, required=False)
    contact = serializers.IntegerField(
        required=False,
        validators=[UniqueValidator(queryset=Profile.objects.all())],
    )

    class Meta:
        model = Profile
        fields = ("name", "bio", "location", "contact", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated-at")

    def update(self, instance, validated_data):
        instance.bio = validated_data.get("bio", instance.bio)
        instance.location = validated_data.get("location", instance.location)
        instance.contact = validated_data("contact", instance.contact)
        instance.save()
        return instance


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):  # type:ignore[no-untyped-def]
        self.token = attrs["refresh"]
        return attrs

    def save(self, **kwargs):  # type:ignore[no-untyped-def]

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:

            raise serializers.ValidationError(
                "Invalid or expired token", code="invalid_token"
            )


class UnitsSerializer(serializers.ModelSerializer):
    """
    serializing the Units model
    Creates a unit and allocates a lecturer
    """

    id = serializers.CharField(
        read_only=True,
    )

    code = serializers.CharField(
        max_length=20,
        min_length=2,
    )
    name = serializers.CharField(
        max_length=400,
        min_length=2,
    )
    lecturer = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field="username"
    )

    class Meta:
        model = Units
        fields = ("id", "code", "name", "lecturer", "created_at")
        read_only_fields = ("id", "created_at")


class RegisteredStudentsSerializer(serializers.ModelSerializer):
    """
    registers students
    """

    id = serializers.CharField(
        read_only=True,
    )

    regnumber = serializers.CharField(
        max_length=30,
        min_length=2,
    )
    sname = serializers.CharField(
        max_length=200,
        min_length=2,
    )

    class Meta:
        model = RegisteredStudents
        fields = ("id", "regnumber", "sname", "created_at")
        read_only_fields = ("id", "created_at")


class StudentUnitsSerializer(serializers.ModelSerializer):
    """
    Allocates units to students
    """

    unit = serializers.SlugRelatedField(queryset=Units.objects.all(), slug_field="code")
    student = serializers.SlugRelatedField(
        queryset=RegisteredStudents.objects.all(), slug_field="regnumber"
    )

    class Meta:
        model = RegisterUnits
        fields = ("id", "unit", "student", "created_at")
        read_only_fields = ("id", "created_at")

    def create(self, validated_data):
        instance, _ = RegisterUnits.objects.get_or_create(**validated_data)
        return instance


class MarkStudentsSerializer(serializers.ModelSerializer):
    student = serializers.SlugRelatedField(
        queryset=RegisteredStudents.objects.all(), slug_field="regnumber"
    )
    unit = serializers.SlugRelatedField(queryset=Units.objects.all(), slug_field="code")
    marked_by = UserSerializer(read_only=True)
    status = serializers.BooleanField(default=True)

    class Meta:
        model = MarkStudents
        fields = ("id", "created_at", "student", "unit", "status", "marked_by")
        read_only_fields = ("id", "marked_by", "created_at")
    def create(self, validated_data):
        request = self.context["request"]
        validated_data["marked_by"] = request.user
        instance = MarkStudents.objects.create(**validated_data)
        return instance


# class ApprovedSerializer(serializers.ModelSerializer):
#     """
#     Approval model serializer
#     """

#     id = serializers.CharField(
#         read_only=True,
#     )
#     # attended_count = serializers.SerializerMethodField()

#     student = serializers.SlugRelatedField(
#         queryset=RegisteredStudents.objects.all(), slug_field="regnumber"
#     )
#     present = serializers.BooleanField(default=True)
#     unit = serializers.SlugRelatedField(queryset=Units.objects.all(), slug_field="code")

#     class Meta:
#         model = Approved
#         fields = (
#             "id",
#             "student",
#             "present",
#             "unit",
#             "total",
#             # "attended_count",
#             "created_at",
#         )
#         read_only_fields = ("id", "total",  "created_at")

#     # def get_attended_count(self,approved: Approved):
#     #     # import pdb; pdb.set_trace()
#     #     return Approved.objects.filter(present=True).values("present").annotate(approved=Count("unit"))
