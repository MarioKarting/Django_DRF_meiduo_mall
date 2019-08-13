from rest_framework import serializers
from orders.models import OrderInfo,OrderGoods
from goods.models import SKU


class SKUSerialzier(serializers.ModelSerializer):
    """
        sku
    """

    class Meta:
        # 指定根据那个模型类生成序列化器字段
        model = SKU
        # 指定那些字段生成
        fields = ('name','default_image')

class OrderGoodsSerialzier(serializers.ModelSerializer):
    """
        订单商品表
    """

    sku=SKUSerialzier()
    class Meta:
        # 指定根据那个模型类生成序列化器字段
        model = OrderGoods
        # 指定那些字段生成
        fields = ('count','price','sku')


class OrderSerializer(serializers.ModelSerializer):
    """
        订单表序列化
    """
    # 关联嵌套序列化返回 USer
    user = serializers.StringRelatedField(read_only=True)
    address = serializers.PrimaryKeyRelatedField(read_only=True)

    # 订单商品表关联订单表
    skus=OrderGoodsSerialzier(many=True)

    class Meta:
        # 指定根据那个模型类生成序列化器字段
        model = OrderInfo
        # 指定那些字段生成

        fields = "__all__"




"""      订单表
        "order_id": "20181126102807000000004",
        "user": "zxc000",
        "total_count": 5,
        "total_amount": "52061.00",
        "freight": "10.00",
        "pay_method": 2,
        "status": 1,
        "create_time": "2018-11-26T18:28:07.470959+08:00",
        skus嵌套订单商品表
        "skus": [
            {
                "count": 1,
                "price": "6499.00",
                sku嵌套sku表
                "sku": {
                    "name": "Apple iPhone 8 Plus (A1864) 64GB 金色 移动联通电信4G手机",
                    "default_image_url": "http://image.meiduo.site:8888/group1/M00/00/02/CtM3BVrRZCqAUxp9AAFti6upbx41220032"
                }
            },
            ......
        ]

"""