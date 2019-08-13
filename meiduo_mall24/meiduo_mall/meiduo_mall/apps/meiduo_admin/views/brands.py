from fdfs_client.client import Fdfs_client
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.conf import settings

from goods.models import Brand
from meiduo_admin.serializers.brands import BrandsSerialzier
from meiduo_admin.utils import PageNum


class BrandsView(ModelViewSet):
    """
            品牌表的增删改查
    """
    permission_class = [IsAdminUser]
    pagination_class = PageNum
    queryset = Brand.objects.all()
    serializer_class = BrandsSerialzier

