from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _
from users.abstracts import TimeStampedModel, UniversalIdModel
from django.db.models.signals import pre_save
from django.dispatch import receiver


class UserManager(BaseUserManager):
    use_in_migrations: True

    def _create_user(self, username: str, email: str, password: str, **kwargs):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError("The given username must be set")
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username: str, email: str, password: str, **kwargs):
        kwargs.setdefault("is_staff", False)
        kwargs.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **kwargs)

    def create_superuser(self, username: str, email: str, password: str, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)

        if not password:
            raise ValueError("Password is required")
        if kwargs.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if kwargs.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **kwargs)


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel, UniversalIdModel):
    """
    The Users Model
    """

    username = models.CharField(
        _("username"),
        max_length=150,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
    )
    email = models.EmailField(
        unique=True,
    )
    name = models.CharField(
        _("name"),
        max_length=200,
    )
    # is_active = models.BooleanField(
    #     _("active"),
    #     default=True,
    #     help_text=_(
    #         "Designates whether this user should be treated as active. "
    #         "Unselect this instead of deleting accounts."
    #     ),
    # )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_verified = models.BooleanField(default=False)

    objects = UserManager()
    REQUIRED_FIELDS = ["username", "password"]
    USERNAME_FIELD = "email"


class Profile(UniversalIdModel):
    """
    User profile model
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add image
    bio = models.CharField(blank=True, max_length=500, null=True)
    location = models.CharField(blank=True, max_length=500, null=True)


class Units(UniversalIdModel, TimeStampedModel):
    """
    Model for units
    """

    code = models.CharField(
        max_length=20,
    )
    name = models.CharField(
        max_length=400,
    )
    lecturer = models.ForeignKey(User, on_delete=models.CASCADE)


class RegisteredStudents(UniversalIdModel, TimeStampedModel):
    """
    model that will contain students
    """

    unit = models.ForeignKey(Units, on_delete=models.CASCADE)
    regnumber = models.CharField(
        max_length=30,
    )
    sname = models.CharField(
        max_length=200,
    )

    class Meta:
        ordering = ["unit"]


class Approved(UniversalIdModel, TimeStampedModel):
    """
    used to mark the students
    """

    student = models.ForeignKey(RegisteredStudents, on_delete=models.CASCADE)
    present = models.BooleanField(default=True)
    unit = models.ForeignKey(Units, on_delete=models.CASCADE)
    total = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        ordering = ["unit", "student", "present", "total",]


@receiver(pre_save, sender=Approved)
def total_pre_save(sender, instance, **kwargs):
    instance.total = Approved.objects.filter(present=True).count()
