from rest_framework import serializers
from rest_framework.response import Response

from goods.models import Brand
from fdfs_client.client import Fdfs_client

from django.conf import settings


class BrandsSerialzier(serializers.ModelSerializer):

    # logo =serializers.CharField()
    class Meta:
        model = Brand
        fields = "__all__"

    def create(self, validated_data):
        # 因为序列化关联sku选项是read_only =True,不参与序列化返回
        # 所以这里采用sefl.context(是个字典数据,保存了请求对象request )获取sku
        id = self.context['request'].data.get('id')
        name = self.context['request'].data.get('name')
        first_letter = self.context['request'].data.get('first_letter')
        '''
        self下的context(字典类型),中有request(objects 是个请求对象,)
        request.data(请求体中的的数据),下有'sku'
        '''
        # 获取保存的图片数据
        logo = validated_data.get('logo')
        # 建立FastDFS的连接对象
        client = Fdfs_client(settings.FASTDFS_CONF)
        # 上传图片数据 read 读取二进制数据通过buffer上传 结果是一个字典
        res = client.upload_by_buffer(logo.read())

        # 判断上传状态
        if res['Status'] != 'Upload successed.':
            raise serializers.ValidationError('图片上传失败')
        # 上传成功 获取返回图片的路径信息
        img_url = res['Remote file_id']
        # 将路径信息保存在图片表
        logo = Brand.objects.create(logo=img_url, id=id, name=name, first_letter=first_letter)

        # 返回图片表对象
        return logo

    def update(self, instance, validated_data):
        # 获取保存的图片数据
        image_data = validated_data.get('logo')
        # 建立FastDFS的连接对象
        client = Fdfs_client(settings.FASTDFS_CONF)
        # 上传图片数据 read 读取二进制数据通过buffer上传 结果是一个字典
        res = client.upload_by_buffer(image_data.read())

        # 判断上传状态
        if res['Status'] != 'Upload successed.':
            raise serializers.ValidationError('图片上传失败')
        # 上传成功 获取返回图片的路径信息
        img_url = res['Remote file_id']

        # 更新图片路径
        instance.logo = img_url
        instance.save()

        # 返回图片表对象
        return instance