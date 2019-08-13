from rest_framework import serializers

from goods.models import SPU, Brand, GoodsCategory


#获取一二三分类
class CategorysSerizliser(serializers.ModelSerializer):
    """
        SPU表分类信息获取序列化器
    """
    class Meta:
        model=GoodsCategory
        fields="__all__"

#获取品牌信息
class SPUBrandsSerizliser(serializers.ModelSerializer):
    """
        SPU表品牌序列化器
    """
    class Meta:
        model = Brand
        fields = "__all__"

#获取sup表首页信息
class SPUGoodsSerialzier(serializers.ModelSerializer):
    """
        SPU表序列化器
    """
    # 一级分类id  category1 = models.ForeignKey(GoodsCategory, on_delete=models.PROTECT, related_name='cat1_spu', verbose_name='一级类别')
    category1_id=serializers.IntegerField()
    # 二级分类id
    category2_id=serializers.IntegerField()
    # 三级级分类id
    category3_id=serializers.IntegerField()
    # 关联的品牌id   # 关联的品牌，名称  brand = models.ForeignKey(Brand, on_delete=models.PROTECT, verbose_name='品牌')
    brand_id=serializers.IntegerField()
    brand=serializers.StringRelatedField(read_only=True)

    class Meta:
        model=SPU
        exclude=('category1','category2','category3')