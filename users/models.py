import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from core.utils.models import TimestampedModel
from django.utils.translation import gettext_lazy as _
from permission.models import Permission
from roles.models import Role

class User(AbstractUser, TimestampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(
        _("First Name"),
        max_length=100,
        help_text="First name of the user"
    )
    last_name = models.CharField(
        _("Last Name"),
        max_length=100,
        help_text="Last name of the user"
    )
    user_role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        null=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name="User Permissions",
        blank=True
    )

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.get_full_name()} ({self.username})"

# import uuid
# from django.db import models
# from django.contrib.auth.models import AbstractUser
# from core.utils.models import TimestampedModel
# from django.utils.translation import gettext_lazy as _
# from permission.models import Permission
# from roles.models import Role

# class User(AbstractUser, TimestampedModel):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     first_name = models.CharField(
#         _("First Name"),
#         max_length=100,
#         help_text="First name of the user"
#     )
#     last_name = models.CharField(
#         _("Last Name"),
#         max_length=100,
#         help_text="Last name of the user"
#     )
#     user_role = models.ForeignKey(
#         Role,
#         on_delete=models.CASCADE,
#         null=True
#     )
#     user_permissions = models.ManyToManyField(
#         Permission,
#         verbose_name="User Permissions",
#         blank=True
#     )

#     def get_full_name(self):
#         return f"{self.first_name} {self.last_name}"

#     class Meta:
#         verbose_name = "User"
#         verbose_name_plural = "Users"

#     def __str__(self):
#         return f"{self.get_full_name()} ({self.username})"
    
