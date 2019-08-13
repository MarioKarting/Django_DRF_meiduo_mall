from rest_framework import serializers
from goods.models import SPUSpecification, SPU


class SpecSerializer(serializers.ModelSerializer):
    """
        商品规格表序列化器
    """
    # 关联嵌套序列化返回
    # 指定返回spu的名称
    spu = serializers.StringRelatedField(read_only=True)
    # 指定spu的id值，根据数据表中的字段最为序列化返回字段
    spu_id = serializers.IntegerField()

    class Meta:
        # 指定根据那个模型类生成序列化器字段
        model = SPUSpecification
        # 指定那些字段生成
        fields = ('id', 'name','spu','spu_id')


class SPUSerializer(serializers.ModelSerializer):
    """
        SPU商品表序列化器
    """

    class Meta:
        # 指定根据那个模型类生成序列化器字段
        model = SPU
        # 指定那些字段生成
        fields = ('id', 'name')