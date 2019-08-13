
from rest_framework import serializers
from goods.models import SKUImage, SPU, SKU
from django.conf import settings
from fdfs_client.client import Fdfs_client
from celery_tasks.detail_html.tasks import get_detail_html

class ImageSerializer(serializers.ModelSerializer):
    """
        图品表序列化器
    """
    # 关联嵌套序列化返回
    sku = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        # 指定根据那个模型类生成序列化器字段
        model = SKUImage
        # 指定那些字段生成
        fields = ('id', 'image', 'sku')

        # 重写原生的保存方法,原生保存的是图片的数据对象,现在原生方法保存的是图片路径

    def create(self, validated_data):
        #因为序列化关联sku选项是read_only =True,不参与序列化返回
        #所以这里采用sefl.context(是个字典数据,保存了请求对象request )获取sku
        sku_id = self.context['request'].data.get('sku')
        '''
        self下的context(字典类型),中有request(objects 是个请求对象,)
        request.data(请求体中的的数据),下有'sku'
        '''
        # 获取保存的图片数据
        image_data = validated_data.get('image')
        # 建立FastDFS的连接对象
        client = Fdfs_client(settings.FASTDFS_CONF)
        # 上传图片数据 read 读取二进制数据通过buffer上传 结果是一个字典
        res=client.upload_by_buffer(image_data.read())

        # 判断上传状态
        if res['Status'] != 'Upload successed.':
            raise serializers.ValidationError('图片上传失败')
        # 上传成功 获取返回图片的路径信息
        img_url = res['Remote file_id']
        # 将路径信息保存在图片表
        image = SKUImage.objects.create(image=img_url, sku_id=sku_id)
        # 调用详情页静态化方法
        sku_id = image.sku.id
        get_detail_html.delay(sku_id)

        # 返回图片表对象
        return image

    def update(self, instance, validated_data):
        # 获取保存的图片数据
        image_data = validated_data.get('image')
        # 建立FastDFS的连接对象
        client = Fdfs_client(settings.FASTDFS_CONF)
        # 上传图片数据 read 读取二进制数据通过buffer上传 结果是一个字典
        res=client.upload_by_buffer(image_data.read())

        # 判断上传状态
        if res['Status'] != 'Upload successed.':
            raise serializers.ValidationError('图片上传失败')
        # 上传成功 获取返回图片的路径信息
        img_url = res['Remote file_id']

        #更新图片路径
        instance.image = img_url
        instance.save()
        # 调用详情页静态化方法
        sku_id = instance.sku.id
        get_detail_html.delay(sku_id)
        # 返回图片表对象
        return instance


class SKUSerializer(serializers.ModelSerializer):
    """
        SPU商品表序列化器
    """

    class Meta:
        # 指定根据那个模型类生成序列化器字段
        model = SKU
        # 指定那些字段生成
        fields = ('id', 'name')

