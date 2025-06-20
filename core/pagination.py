from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
import math

class CustomPagination(PageNumberPagination):
    page_size = 20  # 預設每頁項目數
    page_query_param = 'page'
    page_size_query_param = 'page_size'  # ← 加這行讓前端可設定每頁筆數
    max_page_size = 100  # 可選：限制最大每頁筆數，避免一次抓太多資料

    def get_paginated_response(self, data):
        page_size = self.get_page_size(self.request)
        total_pages = math.ceil(self.page.paginator.count / page_size) if page_size else 0

        return Response({
            'count': self.page.paginator.count,
            'total_pages': total_pages,
            'page': self.page.number,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })
