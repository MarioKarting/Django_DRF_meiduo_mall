# from django.db import models
#
# # Create your models here.
#
#
# # class BookSerialzier():
# #
# #     heroinfo_set
#
# class Bookinfo(models.Model):
#
#     btitl=models.CharField(max_length=11)
#
#
# class BassModel(models.Model):
#     create_time=models.DateField()
#
# class HeroInfo(BassModel):
#
#     book=models.ForeignKey(Bookinfo,on_delete=models.SET_DEFAULT,default='',related_name='hero')
#
#     class Meta:
#         db_table='tb_book'
#         ordering=('-id')
#
#
#
#     def change_data(self):
#         print(11111)
#
#
# # Bookinfo().heroinfo_set.all()
# Bookinfo().hero.all()
#
#
# HeroInfo().change_data()
#
# HeroInfo().Meta.db_table
#
#
