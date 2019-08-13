from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from goods.models import SPU, Brand, GoodsCategory, SKU
from meiduo_admin.serializers.specs import SPUSerializer
from meiduo_admin.serializers.spus import SPUGoodsSerialzier, SPUBrandsSerizliser, CategorysSerizliser
from meiduo_admin.utils import PageNum
from django.conf import settings
from fdfs_client.client import Fdfs_client
#spu表增删改查,一二三级分类
class SPUGoodsView(ModelViewSet):
    """
        SPU表的增删改查
    """
    # 指定权限
    permission_classes = [IsAdminUser]
    # 指定序列化器
    serializer_class = SPUGoodsSerialzier
    # 指定查询及
    queryset = SPU.objects.all()
    # 指定分页
    pagination_class = PageNum

    def get_queryset(self):
        keyword = self.request.query_params.get('keyword')
        if keyword == '' or keyword is None:
            return SPU.objects.all()
        else:
            return SPU.objects.filter(name=keyword)
    # 在类中跟定义获取品牌数据的方法
    def brand(self, request):
        # 1、查询所有品牌数据
        data = Brand.objects.all()
        # 2、序列化返回品牌数据
        ser = SPUBrandsSerizliser(data, many=True)

        return Response(ser.data)

    def channel(self, request):
        # 1、获取一级分类数据
        data = GoodsCategory.objects.filter(parent=None)
        # 2、序列化返回分类数据
        ser = CategorysSerizliser(data, many=True)
        return Response(ser.data)

    def channels(self, request, pk):
        # 1、获取二级和三级分类数据
        data = GoodsCategory.objects.filter(parent_id=pk)
        # 2、序列化返回分类数据
        ser = CategorysSerizliser(data, many=True)
        return Response(ser.data)


class SPUSView(ModelViewSet):
    """
        spu表的增删改查
    """
    serializer_class = SPUSerializer
    queryset = SPU.objects.all()
    pagination_class = PageNum


    def image(self,request):
        """
            保存图片
        :param request:
        :return:
        """
        # 1、获取图片数据
        data = request.FILES.get('image')
        # 验证图片数据
        if data is None:
            return Response(status=500)

        # 2、建立fastDFS连接对象
        client = Fdfs_client(settings.FASTDFS_CONF)

        # 3、上传图片
        res = client.upload_by_buffer(data.read())

        # 4、判断上传状态
        if res['Status'] != 'Upload successed.':
            return Response({'error': '上传失败'}, status=501)

        # 5、获取上传的图片路径
        image_url = res['Remote file_id']

        # 6、结果返回
        return Response(
            {
                'img_url': settings.FDFS_URL+image_url
            },

            status=201
        )