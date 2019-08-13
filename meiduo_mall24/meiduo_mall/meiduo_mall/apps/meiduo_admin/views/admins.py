from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import Group,Permission


from meiduo_admin.serializers.admins import AdminSerializer
from meiduo_admin.serializers.groups import GroupSerializer

from meiduo_admin.utils import PageNum
from users.models import User


# AdminView继承的是ModelViewSet 所以管理员信息修改逻辑还是使用同一个类视图
class AdminView(ModelViewSet):
    serializer_class = AdminSerializer
    queryset = User.objects.filter(is_staff=True)
    pagination_class = PageNum

    # 获取分组数据
    def simple(self, reqeust):
        pers = Group.objects.all()
        ser = GroupSerializer(pers, many=True)
        return Response(ser.data)
