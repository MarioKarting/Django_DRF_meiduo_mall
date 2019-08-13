from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import Permission, ContentType

from meiduo_admin.serializers.permission import PermissionSerializer, ContentTypeSerializer
from meiduo_admin.utils import PageNum


class PermissionView(ModelViewSet):
    """
        权限表增删改查
    """
    # 指定序列化器
    serializer_class = PermissionSerializer
    # 指定查询集
    queryset = Permission.objects.all()
    # 指定分页器
    pagination_class = PageNum
    # 指定权限
    permission_classes = [IsAdminUser]

    # 定义权限类型表操作
    def content_types(self, request):
        # 1、查询所有权限类型
        contenttype = ContentType.objects.all()
        # 2、返回权限类型
        ser = ContentTypeSerializer(contenttype, many=True)
        return Response(ser.data)
