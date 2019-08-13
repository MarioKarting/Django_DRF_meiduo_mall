from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from goods.models import SPU, Brand, GoodsCategory, SKU, GoodsChannel, GoodsChannelGroup
from meiduo_admin.serializers.channels import GoodsChannelSerialzier,CategorysSerizliser,GoodsChannelGroupSerizliser
from meiduo_admin.serializers.specs import SPUSerializer
from meiduo_admin.utils import PageNum
from django.conf import settings
from fdfs_client.client import Fdfs_client


# class channel_typesView(ListAPIView):
#     serializer_class = SPUSimpleSerializer
#     queryset = SPU.objects.all()


#频道表增删改查
class ChannelView(ModelViewSet):

    serializer_class = GoodsChannelSerialzier
    # 指定查询及
    queryset = GoodsChannel.objects.all()
    # 指定分页
    pagination_class = PageNum


    def categories(self, request):
        # 1、获取一级分类数据
        data = GoodsCategory.objects.filter(parent=None)
        # 2、序列化返回分类数据
        ser = CategorysSerizliser(data, many=True)
        return Response(ser.data)

    def channel_types(self, request):
        # 1、获取频道组名字
        data = GoodsChannelGroup.objects.all()
        # 2、序列化返回分类数据
        ser = GoodsChannelGroupSerizliser(data,many=True)
        return Response(ser.data)


