from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from meiduo_admin.serializers.specs import SpecSerializer, SPUSerializer
from meiduo_admin.utils import PageNum
from goods.models import SPUSpecification, SPU


class SpecView(ModelViewSet):
    """
        规格表的增删改查
    """
    # 指定序列化器
    serializer_class = SpecSerializer
    # 指定查询集
    queryset = SPUSpecification.objects.all()
    # 指定分页器
    pagination_class = PageNum
    # 指定权限
    permission_classes = [IsAdminUser]

    # 获取spu的商品信息
    def simple(self, reqeust):
        # 1、查询所有spu信息
        spus = SPU.objects.all()
        # 2、结果返回
        ser = SPUSerializer(spus, many=True)
        return Response(ser.data)
