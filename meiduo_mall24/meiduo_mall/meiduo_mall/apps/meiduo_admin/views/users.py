from rest_framework.generics import ListAPIView,CreateAPIView,ListCreateAPIView
from rest_framework.permissions import IsAdminUser
from meiduo_admin.serializers.users import UserSerializer
from meiduo_admin.utils import PageNum
from users.models import User


class UserView(ListCreateAPIView):
    """
        用户表的获取和保存
    """
    # 指定序列化器
    serializer_class = UserSerializer
    # 指定查询集
    queryset = User.objects.filter(is_staff=False)
    # 指定分页器
    pagination_class = PageNum
    # 指定权限
    permission_classes = [IsAdminUser]

    # 重写get_queryset方法根据前端传递的keyword参数，返回不同的数据
    def get_queryset(self):
        # 1、获取前端的keyword参数
        keyword = self.request.query_params.get('keyword')
        if keyword == '':
            return User.objects.filter(is_staff=False)
        else:
            # username__contains 模糊查询 包含
            return User.objects.filter(is_staff=False, username__contains=keyword)
