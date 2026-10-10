from shop.models import SellerProfile, CustomerProfile
from django.core.exceptions import PermissionDenied

#authentications
def _is_admin(user):
    return user.is_authenticated and user.is_superuser

def _require_admin(request):
    if not _is_admin(request.user):
        raise PermissionDenied

def _require_seller(request):
    if not SellerProfile.objects.filter(user=request.user).exists():
        raise PermissionDenied

def _require_customer(request):
    customer = CustomerProfile.objects.filter(user=request.user).first()
    if customer is None:
        raise PermissionDenied
    return customer