
# permissions.py
import logging
from rest_framework.permissions import BasePermission

logger = logging.getLogger(__name__)
class IsMerchantUser(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'adminuser')  # 判斷是否為商家或管理員

    def has_object_permission(self, request, view, obj):
        adminuser = getattr(request.user, 'adminuser')
        return obj.merchant.user == request.user or adminuser.role == 'manager'  # 商家只能修改自己的商品
