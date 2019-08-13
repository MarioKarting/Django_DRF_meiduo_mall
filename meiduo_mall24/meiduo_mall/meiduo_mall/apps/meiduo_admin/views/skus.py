from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from goods.models import SKU, GoodsCategory,SPU
from meiduo_admin.serializers.skus import SKUSerializer,GoodsCategorySerializer,SPUSpecificationSerialzier
from meiduo_admin.utils import PageNum


class SKUView(ModelViewSet):
    """
        sku增删改查
    """
    # 指定序列化器
    serializer_class = SKUSerializer
    # 指定查询集
    queryset = SKU.objects.all()
    # 指定分页器
    pagination_class = PageNum
    # 指定权限
    permission_classes = [IsAdminUser]
    # 重写get_queryset方法，判断是否传递keyword查询参数
    def get_queryset(self):
          # 提取keyword
        keyword=self.request.query_params.get('keyword')

        if keyword == '' or keyword is None:
            return SKU.objects.all()
        else:
            return SKU.objects.filter(name__contains=keyword)

    # 获取sku的所有三级分类信息
    @action(methods=['get'], detail=False)
    def categories(self, request):
        # 查询分类表获取三级分类
        # goods = GoodsCategory.objects.filter(id__gte=115)
        goods = GoodsCategory.objects.filter(subs=None)
        # 返回三级分类数据
        ser = GoodsCategorySerializer(goods, many=True)
        return Response(ser.data)

    # 获取商品的相关规格信息
    def specs(self, reuqest, pk):
        # 根据pk值先查查询spu商品
        spu = SPU.objects.get(id=pk)
        # 根据spu商品对象返回规格和规格选贤
        spec = spu.specs.all()
        # 返回规格数据
        ser = SPUSpecificationSerialzier(spec, many=True)
        return Response(ser.data)

