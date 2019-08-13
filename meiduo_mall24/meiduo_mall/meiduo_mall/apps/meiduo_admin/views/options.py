from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from goods.models import SpecificationOption, SPUSpecification
from meiduo_admin.serializers.options import OptionSerialzier, SPUSpecificationSerializer
from meiduo_admin.utils import PageNum


class OptionsView(ModelViewSet):
    """
            规格选项表的增删改查
    """
    # 指定权限
    permission_classes = [IsAdminUser]
    serializer_class = OptionSerialzier
    queryset = SpecificationOption.objects.all()
    pagination_class = PageNum

    # 获取option的商品信息
    def simple(self, reqeust):
        # 1、查询所有选项信息
        options = SPUSpecification.objects.all()
        # 2、结果返回
        ser = SPUSpecificationSerializer(options, many=True)
        return Response(ser.data)