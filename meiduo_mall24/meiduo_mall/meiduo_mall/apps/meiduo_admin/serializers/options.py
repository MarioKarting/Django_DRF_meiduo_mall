from rest_framework import serializers

from goods.models import SpecificationOption, SPUSpecification


#获取规格选项
class SPUSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        # 指定根据那个模型类生成序列化器字段
        model =  SPUSpecification
        # 指定那些字段生成
        fields = ('id', 'name')

#规格选项首页
class OptionSerialzier(serializers.ModelSerializer):
    # 嵌套返回规格名称
    spec = serializers.StringRelatedField(read_only=True)
    # 返回规格id
    spec_id = serializers.IntegerField()

    class Meta:
        model = SpecificationOption  # 规格选项表中的spec字段关联了规格表
        fields = "__all__"
