from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from meiduo_admin.serializers.orders import OrderSerializer
from goods.models import SKUImage, SPU, SKU
from meiduo_admin.utils import PageNum
from orders.models import OrderInfo
from rest_framework.decorators import action


class OrderView(ReadOnlyModelViewSet):
    """
        图片表的增删改查
    """
    permission_classes = [IsAdminUser]
    # 指定序列化器
    serializer_class = OrderSerializer
    # 指定查询集
    # queryset = SKUImage.objects.all()
    # 指定分页器
    pagination_class = PageNum
    # 指定权限


    # 重写get_queryset方法根据前端传递的keyword参数，返回不同的数据
    def get_queryset(self):
        # 1、获取前端的keyword参数
        keyword = self.request.query_params.get('keyword')
        if keyword == '' or keyword is None:
            return OrderInfo.objects.all()
        else:
            # username__contains 模糊查询 包含
            return OrderInfo.objects.filter(order_id__contains=keyword)

            # 修改订单状态

    @action(methods=['put'], detail=True)
    def status(self, request, pk):
        # 1、查询订单对象
        try:
            order = OrderInfo.objects.get(order_id=pk)
        except:
            return Response({"error": "无效的订单编号"})
        # 2、修改订单状态
        status = request.data.get('status')
        if status is None:
            return Response({"error": "缺少订单状态"})
        order.status = status
        order.save()
        # 3、返回订单信息
        ser = self.get_serializer(order)
        return Response(ser.data)
