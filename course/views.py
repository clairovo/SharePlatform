import logging
import os
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CourseSerializers
from login.login_token import *
from .models import Course
from rest_framework.viewsets import ModelViewSet
from SharePlatform.settings import MEDIA_ROOT

# Create your views here.
""""
创建课程的视图函数
"""


class CourseView(APIView):
    path = os.path.join(MEDIA_ROOT,os.path.join('images','course'))
    baseUrl = 'http://192.168.0.105:8000/media/'
    @resolve_token
    def post(self,request,args):
        data = {'code': 401}
        course = request.data.copy()           # query_dict不可变，从此需要copy
        course['owner_id'] = args.get('uid')  # 创建人的uid
        #course['owner_name'] = args.get('name')  # 创建人的name
        image_name= os.path.split(course.get('image'))[1]
        course['image'] = 'images/course' + '/' + image_name
        if args.get('role',None) == 'student':
            data['msg'] = 'sorry,only teacher can create course!'
            return Response(data,status=401)
        # #  图片写入磁盘
        # image = request.FILES.get('image',None)
        # if image is not None:
        #     destination = open(os.path.join(self.path, image.name), 'wb')
        #     print('文件名：' + image.name + '\n' + '文件大小：' + str(image.size / 1024) + 'KB')
        #     for chunk in image.chunks():
        #         destination.write(chunk)
        #     destination.close()
        #     course['image'] = 'images/course'+'/'+image.name
        serializer = CourseSerializers(data=course)
        try:
            if serializer.is_valid(raise_exception=True):
                current = serializer.save()
                data['code'] = 201
                data['msg'] = '创建成功！'
                data['id'] = current.id
                return Response(data,status=201)
        except Exception as e:
            print(e)
        data['msg'] = '该课程已存在!'
        return Response(data,status=401)

    def get(self,request):
        page = request.query_params.get('current')
        limit = request.query_params.get('limit')
        query = request.data.get('query')
        courses = Course.objects.all()
        paginator = Paginator(courses, limit)  # 分别是需要分页的数据 和多少行数据为一页
        pag_count = paginator.num_pages  # 获取整个表的总页数
        if pag_count < int(page):
            return Response({'code':400,'msg':'请求参数有误'},status=400)
        current_page = paginator.page(page)  # 获取当前页的数据
        serializers = CourseSerializers(current_page,many=True)
        return Response({'code':200,'data':serializers.data,'msg':'获取课程列表成功','total':len(courses)},status=200)


class CourseObjectView(ModelViewSet):
    baseUrl = 'http://192.168.0.105:8000/media/'
    permission_classes = []
    queryset = Course.objects.all()
    serializer_class = CourseSerializers

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.image = self.baseUrl+instance.image
        serializer = self.get_serializer(instance)
        return Response({'code': 200, 'msg': '获取课程信息成功！', 'data': serializer.data}, status=200)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        print(request.data)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response({'code': 200, 'msg': '修改课程信息成功！', 'data': serializer.data}, status=200)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'code': 200, 'msg': '删除课程成功！'},status=204)


class CourseRecommend(APIView):
    baseUrl = 'http://192.168.0.105:8000/media/'
    def get(self, request):

        courses = Course.objects.all()
        for course in courses:
            course.image=self.baseUrl+course.image
        serializers = CourseSerializers(courses, many=True)
        return Response({'code': 200, 'data': serializers.data, 'msg': '获取课程列表成功'}, status=200)


class CourseUpload(APIView):
    permission_classes = []
    baseUrl = 'http://192.168.0.105:8000/media/'
    path = os.path.join(MEDIA_ROOT, os.path.join('images', 'course'))
    logger = logging.getLogger('course.views')

    def post(self,request):
        #  图片写入磁盘
        image = request.FILES.get('file', None)
        print(image.name)
        if image is not None:
            destination = open(os.path.join(self.path, image.name), 'wb')
            print('文件名：' + image.name + '\n' + '文件大小：' + str(image.size / 1024) + 'KB')
            for chunk in image.chunks():
                destination.write(chunk)
            destination.close()
            img_url = self.baseUrl+'images/course'+'/'+image.name
            self.logger.info('上传'+image.name+'成功！')
            return Response({'code':200,'msg':'上传成功！','image':img_url},status=200)
        else:
            return Response({'code':400,'msg':'上传失败！'},status=400)




















