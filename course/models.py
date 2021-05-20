import datetime
from mongoengine import *
# Create your models here.

"""
课程实体类
"""


class Course(Document):
    id = SequenceField(primary_key=True)  # 自增id ,主码
    cno = SequenceField(unique=True,verbose_name='课程号')
    name = StringField(max_length=20,default='Python')
    overview = StringField(max_length=200,default='课程概述')
    owner_id = IntField(verbose_name='创建人id')  # 教师的uid
    owner_name = StringField(max_length=20,verbose_name='创建人姓名',default='teacher')  # 教师的name
    creat_time = StringField(max_length=50, verbose_name='创建时间',
                             default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    meta = {'collection': 'course'}  # 数据库中的集合

