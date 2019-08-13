from rest_framework import serializers
from goods.models import Brand, GoodsChannel, GoodsChannelGroup

from goods.models import SPU, Brand, GoodsCategory



class GoodsChannelGroupSerizliser(serializers.ModelSerializer):
    """
        SPU表分类信息获取序列化器
    """
    class Meta:
        model=GoodsChannelGroup
        fields="__all__"


#获取一二三分类和分类名
class CategorysSerizliser(serializers.ModelSerializer):
    """
        SPU表分类信息获取序列化器
    """
    class Meta:
        model=GoodsCategory
        fields="__all__"



class GoodsChannelSerialzier(serializers.ModelSerializer):


    #分类名 category
    category = serializers.StringRelatedField(read_only=True)
    #一级分类 category_id
    category_id = serializers.IntegerField()
    #组id
    group_id = serializers.IntegerField()
    #组名
    group =serializers.StringRelatedField(read_only=True)
    class Meta:

        model = GoodsChannel
        fields = "__all__"