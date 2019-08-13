from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import Group,Permission

from meiduo_admin.serializers.groups import GroupSerializer
from meiduo_admin.serializers.permission import PermissionSerializer, ContentTypeSerializer
from meiduo_admin.utils import PageNum


class GroupView(ModelViewSet):
    """
        权限表增删改查
    """
    # 指定序列化器
    serializer_class = GroupSerializer
    # 指定查询集
    queryset = Group.objects.all()
    # 指定分页器
    pagination_class = PageNum
    # 指定权限
    permission_classes = [IsAdminUser]

    # 获取所有权限
    def simple(self, request):
        # 1、查询所有权限类型
        permssion = Permission.objects.all()
        # 2、返回权限类型
        ser = PermissionSerializer(permssion, many=True)
        return Response(ser.data)
