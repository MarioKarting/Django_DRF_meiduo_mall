from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from datetime import date, timedelta

from meiduo_admin.views.serializers import GoodsSerializer
from users.models import User
from goods.models import GoodsVisitCount


#6.1日分类商品访问量(序列化器方法)
class GoodsDayView(APIView):

    def get(self,request):
        # 获取当天日期
        now_date=date.today()
        # 获取当天访问的商品分类数量信息
        goods = GoodsVisitCount.objects.filter(date__gte=now_date)
        print(goods)
        # 序列化返回分类数量
        ser=GoodsSerializer(goods,many=True)
        print(ser)
        return Response(ser.data)

# 6.2日分类商品访问量(APIview)
class GoodsCountView(APIView):
    """
        商品分类访问量统计
    """
    # 权限指定
    permission_classes = [IsAdminUser]

    def get(self, request):
        # 获取当天日期
        now_date = date.today()
        # 获取商品分类访问量
        goods = GoodsVisitCount.objects.filter(date__gte=now_date)
        data_list=[]
        for good in goods:
            count = good.count
            # 获取关联分类对象的名字
            category = good.category.name
            data_list.append({"count":count,'category':category})
        # 返回数量
        return Response(data_list)

#5.日分类商品访问量月增用户统计
class UserMonthCountView(APIView):
    # 权限指定
    permission_classes = [IsAdminUser]

    def get(self, request):
        # 获取当天日期
        now_date = date.today()
        # 获取30天之前的日期
        old_date = now_date - timedelta(29)
        # 遍历，从30之前开始遍历查询每天的用户注册量
        data_list = []
        for i in range(30):
            # 起始日期
            index_date = old_date + timedelta(i)
            # 起始日期的下一天日期
            next_date = old_date + timedelta(i + 1)
            count = User.objects.filter(is_staff=False, date_joined__gte=index_date, date_joined__lt=next_date).count()
            data_list.append({'count': count, 'date': index_date})
        # 返回数量
        return Response(data_list)

#4.日下单用户量统计
class UserOrderCountView(APIView):
    # 指定管理员权限
    permission_classes = [IsAdminUser]
    def get(self, request):
        # 获取当天日期
        now_date = date.today()
        # 获取当天下单用户总数（普通用户）  关联过滤查询 以订单表的数据作为用户表的查询条件
        users = User.objects.filter(is_staff=False, orders__create_time__gte=now_date)
        # 去重
        user = set(users)
        count = len(user)
        # 返回数量
        return Response({'count': count})

#3.日活跃用户统计
class UserActiveCountView(APIView):
    # 权限指定
    permission_classes = [IsAdminUser]

    def get(self, request):
        # 获取当天日期
        now_date = date.today()
        # 获取当天登录用户总数（普通用户）
        count = User.objects.filter(is_staff=False, last_login__gte=now_date).count()
        # 返回数量
        return Response({'count': count, 'date': now_date})

#2.日增用户统计
class UserDayCountView(APIView):
    #指定管理员权限
    permission_classes = [IsAdminUser]

    def get(self,request):
        #获取当前时间
        now_date = date.today()
        #获取当日注册用户数量 date_joined 记录创建账户的时间
        count = User.objects.filter(is_staff=False, date_joined__gte=now_date).count()
        return Response({'count': count, 'date': now_date})

#1.用户总量统计
class UserTotalCountView(APIView):
    # 指定管理员权限
    permission_classes = [IsAdminUser]
    #获取用户总量的方法
    def get(self,request):
        #获取当前日期
        now_date = date.today()
        #获取所有用户总数量
        count = User.objects.filter(is_staff=False).count()
        return Response({'count':count,'date':now_date})