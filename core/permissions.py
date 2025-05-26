
# permissions.py
from rest_framework.permissions import BasePermission

class IsMerchantUser(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'adminuser')  # 判斷是否為商家或管理員

    def has_object_permission(self, request, view, obj):
        return obj.merchant.user == request.user  # 商家只能修改自己的商品
