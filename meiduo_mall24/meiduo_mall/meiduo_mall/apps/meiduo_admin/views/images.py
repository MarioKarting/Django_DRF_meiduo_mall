from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from meiduo_admin.serializers.images import ImageSerializer,SKUSerializer
from meiduo_admin.utils import PageNum
from goods.models import SKUImage, SPU, SKU


class ImageView(ModelViewSet):
    """
        图片表的增删改查
    """
    # 指定序列化器
    serializer_class = ImageSerializer
    # 指定查询集
    queryset = SKUImage.objects.all()
    # 指定分页器
    pagination_class = PageNum
    # 指定权限
    permission_classes = [IsAdminUser]

    # 获取spu的商品信息
    def simple(self, reqeust):
        # 1、查询所有spu信息
        skus = SKU.objects.all()
        # 2、结果返回
        ser = SKUSerializer(skus, many=True)
        return Response(ser.data)