from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from users.models import Profile, Units, RegisteredStudents, Approved
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


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

    username = serializers.CharField(read_only=True, source="user.username")
    bio = serializers.CharField(allow_blank=True, required=False)
    location = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = Profile
        fields = ("username", "bio", "location", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated-at")

    def update(self, instance, validated_data):
        instance.bio = validated_data.get("bio", instance.bio)
        instance.location = validated_data.get("location", instance.location)
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
    students registered for a specific unit
    """

    id = serializers.CharField(
        read_only=True,
    )

    unit = serializers.SlugRelatedField(queryset=Units.objects.all(), slug_field="code")
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
        fields = ("id", "unit", "regnumber", "sname", "created_at")
        read_only_fields = ("id", "created_at")


class ApprovedSerializer(serializers.ModelSerializer):
    """
    Approval model serializer
    """

    id = serializers.CharField(
        read_only=True,
    )

    student = serializers.SlugRelatedField(
        queryset=RegisteredStudents.objects.all(), slug_field="regnumber"
    )
    present = serializers.BooleanField(default=True)
    unit = serializers.SlugRelatedField(
        queryset=Units.objects.all(), slug_field="code"
    )

    class Meta:
        model = Approved
        fields = ("id", "student", "present", "unit", "total", "created_at",)
        read_only_fields = ("id", "total", "created_at")
