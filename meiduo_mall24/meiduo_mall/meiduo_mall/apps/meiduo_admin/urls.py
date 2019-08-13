from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.routers import DefaultRouter
from .views import statistical,users,specs,images,skus,orders,permission,groups,admins
from .views import spus,options,brands,channels

urlpatterns = [
    url(r'^authorizations/$', obtain_jwt_token),
#--------------------------数据统计--------------------------
    # 1.用户总量统计
    url(r'^statistical/total_count/$', statistical.UserTotalCountView.as_view()),
    # 2.当天注册用户总量统计
    url(r'^statistical/day_increment/$', statistical.UserDayCountView.as_view()),
    # 3.当天登录用户总量统计
    url(r'^statistical/day_active/$', statistical.UserActiveCountView.as_view()),
    # 4.当天下单用户总量统计
    url(r'^statistical/day_orders/$', statistical.UserOrderCountView.as_view()),
    # 5.月增用户总量统计
    url(r'^statistical/month_increment/$', statistical.UserMonthCountView.as_view()),
    # 6.1商品分类访问量统计 序列化器方法
    url(r'^statistical/goods_day_views/$', statistical.GoodsDayView.as_view()),
    # 6.2商品分类访问量统计 APIView
    # url(r'^statistical/goods_day_views/$', statistical.GoodsCountView.as_view()),
#--------------------------用户管理--------------------------
    url(r'^users/$', users.UserView.as_view()),
    # ------------------商品规格表管理------------------
    url(r'^goods/simple/$', specs.SpecView.as_view({'get': 'simple'})),
    # ------------------商品图片规格表管理------------------
    url(r'^skus/simple/$', images.ImageView.as_view({'get': 'simple'})),
    # ------------------sku表管理------------------
    url(r'^goods/(?P<pk>\d+)/specs/$', skus.SKUView.as_view({'get': 'specs'})),
    # ------------------spu表管理------------------
    #品牌
    url(r'^goods/brands/simple/$', spus.SPUGoodsView.as_view({'get': 'brand'})),
    #一级分类
    url(r'^goods/channel/categories/$', spus.SPUGoodsView.as_view({'get': 'channel'})),
    #二级,三级分类
    url(r'^goods/channel/categories/(?P<pk>\d+)/$', spus.SPUGoodsView.as_view({'get': 'channels'})),
    #上传图片
    url(r'^goods/images/$', spus.SPUSView.as_view({'post': 'image'})),

    # -----------------权限表管理------------------
    url(r'^permission/content_types/$', permission.PermissionView.as_view({'get': 'content_types'})),
    # -----------------用户组表管理------------------
    url(r'^permission/simple/$', groups.GroupView.as_view({'get': 'simple'})),
    # -----------------管理员表管理------------------
    url(r'^permission/groups/simple/$', admins.AdminView.as_view({'get': 'simple'})),
    # -----------------规格选项表管理------------------
    url(r'^goods/specs/simple/$', options.OptionsView.as_view({'get': 'simple'})),

    # ------------------频道管理------------------
    # 获取频道首页
    url(r'^goods/channels/$', channels.ChannelView.as_view({'get': 'list','post': 'create'})),

    #一级分类
    url(r'^goods/categories/$', channels.ChannelView.as_view({'get': 'categories'})),

    #频道组
    url(r'^goods/channel_types/$', channels.ChannelView.as_view({'get': 'channel_types'})),

    # 品牌管理
    url(r'^goods/brands/$',brands.BrandsView.as_view({'get': 'list','post': 'create'})),

]

# ------------------商品规格表管理------------------

router = DefaultRouter()
router.register('goods/specs', specs.SpecView, base_name='spec')
urlpatterns += router.urls

# ------------------商品图片表管理------------------

router = DefaultRouter()
router.register('skus/images', images.ImageView, base_name='image')
urlpatterns += router.urls

# ------------------sku表管理------------------

router = DefaultRouter()
router.register('skus', skus.SKUView, base_name='skus')
urlpatterns += router.urls

# ------------------spu表管理------------------

router = DefaultRouter()
router.register('goods', spus.SPUGoodsView, base_name='goods')
urlpatterns += router.urls


# ------------------订单表管理------------------

router = DefaultRouter()
router.register('orders', orders.OrderView, base_name='orders')
urlpatterns += router.urls

# -----------------权限表管理------------------

router = DefaultRouter()
router.register('permission/perms', permission.PermissionView, base_name='perms')
urlpatterns += router.urls

# -----------------分组表管理------------------

router = DefaultRouter()
router.register('permission/groups', groups.GroupView, base_name='perms')
urlpatterns += router.urls

# -----------------管理表管理------------------

router = DefaultRouter()
router.register('permission/admins', admins.AdminView, base_name='admins')
urlpatterns += router.urls

# -----------------规格选项表管理------------------

router = DefaultRouter()
router.register('specs/options', options.OptionsView, base_name='options')
urlpatterns += router.urls

# # -----------------品牌表管理------------------

router = DefaultRouter()
router.register('goods/brands', brands.BrandsView, base_name='brands')
urlpatterns += router.urls

# -----------------频道表管理------------------

router = DefaultRouter()
router.register('goods/channels',channels.ChannelView, base_name='channels')
urlpatterns += router.urls

