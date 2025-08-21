
# permissions.py
import logging
from rest_framework.permissions import BasePermission

logger = logging.getLogger(__name__)

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        adminuser = getattr(request.user, 'adminuser')
        return adminuser.role == 'manager'  # 判斷是否為商家或管理員
    
    def has_object_permission(self, request, view, obj):
        adminuser = getattr(request.user, 'adminuser')
        return adminuser.role == 'manager'
class IsMerchantUser(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'adminuser')  # 判斷是否為商家或管理員

    def has_object_permission(self, request, view, obj):
        adminuser = getattr(request.user, 'adminuser')
        return obj.merchant.user == request.user or adminuser.role == 'manager'  # 商家只能修改自己的商品

class IsCustomerUser(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'customer')  # 判斷是否為消費者

    def has_object_permission(self, request, view, obj):
        # customer = getattr(request.user, 'customer')
        return obj.customer == request.user