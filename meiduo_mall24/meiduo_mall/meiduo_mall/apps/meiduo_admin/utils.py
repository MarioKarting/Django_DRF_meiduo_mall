
#Jwt认证
from rest_framework.response import Response


def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义jwt认证成功返回数据
    """
    return {
        'token': token,
        'id': user.id,
        'username': user.username
    }

from rest_framework.pagination import PageNumberPagination

class PageNum(PageNumberPagination):
    '''
      自定义分页器
    '''
    page_size_query_param = 'pagesize'
    max_page_size = 8

    def get_paginated_response(self, data):
        # return Response(OrderedDict([
        #     ('count', self.page.paginator.count),
        #     ('next', self.get_next_link()),
        #     ('previous', self.get_previous_link()),
        #     ('results', data)
        # ]))

        return Response({
            'count': self.page.paginator.count,
            'lists': data,
            "page": self.page.number,
            "pages": self.page.paginator.num_pages,
            "pagesize": self.max_page_size
        })
