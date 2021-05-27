#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File        :   login_token.py    
@CopyRight   :   USTC SSE
@Modify Time :   2020/11/17 19:36
@Author      :   TJ
@Version     :   1.0
@Description :   自定义登录验证类
"""
import jwt
import datetime
import logging as logger
from django.utils import timezone
from SharePlatform import settings


class Authenticated:  # 无需继承其他认证类

    @staticmethod
    def has_permission(request,view):   # 必须是这个名字,必须多带一个没用的view参数
        """
        :param request: 请求
        :param view: 视图函数
        :return: 是否登录（true or false)
        """
        token = request.META.get('HTTP_TOKEN')
        if token:
            BOOLEAN=verify_token(token=token)  # 验证成功返回True 失效及错误token 返回False
            return BOOLEAN
        else:
            BOOLEAN=False
            return BOOLEAN


def verify_token(token):
    """
    :param token: 验证请求的token是否有效
    :return: True or False
    """
    try:
        decode = jwt.decode(token, settings.SECRET_KEY , algorithms=['HS256'])
        logger.debug(decode.get('username'))
        logger.debug(decode.get('uid'))
        #print(decode.get('username'))
        return True
    except Exception as e:
        # '签名已过期
        print(e)
        print('签名已过期')
        return False


def resolve_token(func):
    """
    解析token的装饰器函数
    :param func:
    :return: dict{} 用户信息
    """
    def resolve_token1(self,request):
        token = request.META.get('HTTP_TOKEN')
        args ={}
        try:
            decode = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            args['uid'] = decode.get('uid')
            args['username'] = decode.get('username')
            args['name'] = decode.get('name')
            args['role'] = decode.get('role')
        except Exception as e:
            print(e)
            print('签名已过期')
        return func(self,request,args)
    return resolve_token1


def create_token(user,role):
    """
    创建token,将用户信息存储在token中
    :param user: 用户对象
    :param role: student or teacher
    :return: token
    """
    payload = {"exp": timezone.now()+datetime.timedelta(hours=1), "uid": user.uid, "username": user.username,
               "name": user.name, 'role': role}
    token = jwt.encode(payload,settings.SECRET_KEY , algorithm='HS256').decode('utf8')
    return token


