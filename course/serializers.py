#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File        :   serializers.py    
@CopyRight   :   USTC SSE
@Modify Time :   2020/11/23 15:37
@Author      :   TJ
@Version     :   1.0
@Description :   课程的序列化类
"""
from rest_framework_mongoengine import serializers
from .models import Course


class CourseSerializers(serializers.DocumentSerializer):

    class Meta:
        model = Course
        fields = '__all__'

