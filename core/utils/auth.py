from rest_framework_simplejwt.authentication import JWTAuthentication
from core.utils.permissions import IsHotelPermission
from core.utils.sso_middleware import SSOAuthentication

class MarketplacePermissionMixin(object):
    authentication_classes = (SSOAuthentication,)
    permission_classes = (IsHotelPermission,)
    

class NoAuthRequired(object):
    authentication_classes = ()
    permission_classes = ()


__all__ = [
    "HotelPermissionMixin",
    "NoAuthRequired",
]