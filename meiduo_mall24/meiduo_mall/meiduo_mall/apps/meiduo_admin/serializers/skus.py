from django.db import transaction
from rest_framework import serializers

from goods.models import SKU, SKUSpecification, GoodsCategory, SPUSpecification, SpecificationOption


#3.1具体选项的序列化器
class OptionSerialzier(serializers.ModelSerializer):
    """
        规格选项序列化器
    """

    class Meta:
        # 指定根据那个模型类生成序列化器字段
        model = SpecificationOption
        # 指定那些字段生成
        fields = ('id', 'value')

#3.获取SUP的规格表
class SPUSpecificationSerialzier(serializers.ModelSerializer):
    """
        SPU规格表
         "id": "规格id",
        "name": "规格名称",
        "spu": "SPU商品名称",
        "spu_id": "SPU商品id",
        "options": [
                {
                    "id": "选项id",
                    "name": "选项名称"
                },
                ...
    """
    spu = serializers.StringRelatedField(read_only=True)
    spu_id = serializers.IntegerField()
    # 关联的规格选项表
    options = OptionSerialzier(many=True)

    class Meta:
        # 指定根据那个模型类生成序列化器字段
        model = SPUSpecification
        # 指定那些字段生成
        fields = "__all__"


#2.获取三级分类表
class GoodsCategorySerializer(serializers.ModelSerializer):
    """
        商品分类序列化器
    """

    class Meta:
        # 指定根据那个模型类生成序列化器字段
        model = GoodsCategory
        # 指定那些字段生成
        fields = "__all__"

#1.1定义具体规格表的序列化器
class SKUSpecificationSeriazier(serializers.ModelSerializer):
    """
        sku具体规格表序列化器
    """
    spec_id = serializers.IntegerField()
    option_id = serializers.IntegerField()

    class Meta:
        # 指定根据那个模型类生成序列化器字段
        model = SKUSpecification
        # 指定那些字段生成
        fields = ('spec_id','option_id')

#1.获取sku表
class SKUSerializer(serializers.ModelSerializer):
    """
        sku表序列化器

         "id": "商品SKU ID",
        "name": "商品SKU名称",
        "spu": "商品SPU名称",
        "spu_id": "商品SPU ID",
        "caption": "商品副标题",
        "category_id": "三级分类id",
        "category": "三级分类名称",
        "price": "价格",
        "cost_price": "进价",
        "market_price": "市场价格",
        "stock": "库存",
        "sales": "销量",
        "is_launched": "上下架",
        "specs": [
            {
                "spec_id": "规格id",
                "option_id": "选项id"
            },
            ...
        ]
    """

    # 关联嵌套序列化返回
    #"spu": "商品SPU名称",
    spu = serializers.StringRelatedField(read_only=True)
    #"spu_id": "商品SPU ID",
    spu_id = serializers.IntegerField()
    #"category": "三级分类名称",
    category = serializers.StringRelatedField(read_only=True)
    #"category_id": "三级分类id",
    category_id = serializers.IntegerField()

    #返回主表SKU的附表的skuspecs字段
    # 返回关联的sku具体规格表数据
    specs = SKUSpecificationSeriazier(many=True)

    class Meta:
        # 指定根据那个模型类生成序列化器字段
        model = SKU
        # 指定那些字段生成
        fields = "__all__"


    # 重写保存方法
    def create(self, validated_data):
        #使用事务
        with transaction.atomic():
            #设置保存点
            save_point = transaction.savepoint()
            try:
                #1.保存sku表,取出specs字段
                specs = validated_data['specs']
                #删除 验证数据后的specs字段
                del validated_data['specs']
                sku = SKU.objects.create(**validated_data)
                #2.sku具体规格表,取出spec_id,option_id
                for spec in specs:
                    SKUSpecification.objects.create(
                        sku=sku,
                        spec_id=spec['spec_id'],
                        option_id=spec['option_id'])

            except Exception as e:
                print(e)
                #捕获异常回滚到保存点
                transaction.savepoint_rollback(save_point)
                raise serializers.ValidationError('保存数据失败')
            else:
                #事务提交
                transaction.savepoint_commit(save_point)
                return sku

    # 重写更新方法
    def update(self, instance, validated_data):
        # 使用事务
        with transaction.atomic():
            # 设置保存点
            save_point = transaction.savepoint()
            try:
                # 1.保存sku表,取出specs字段
                specs = validated_data['specs']
                # 删除 验证数据后的specs字段
                del validated_data['specs']
                # sku = SKU.objects.create(**validated_data)
                SKU.objects.filter(id=instance.id).update(**validated_data)
                # 2.sku具体规格表,取出spec_id,option_id
                for spec in specs:
                    SKUSpecification.objects.filter(
                        sku=instance,
                        spec_id=spec['spec_id']).update(option_id=spec['option_id'])


            except Exception as e:
                print(e)
                # 捕获异常回滚到保存点
                transaction.savepoint_rollback(save_point)
                raise serializers.ValidationError('保存数据失败')
            else:
                # 事务提交
                transaction.savepoint_commit(save_point)
                return instance