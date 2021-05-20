from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import StudentSerializers,TeacherSerializers
from login.login_token import *
from .models import *
from course.models import Course
from course.serializers import CourseSerializers
# Create your views here.


class UserView(APIView):
    # 修改用户信息
    @resolve_token
    def get(self,request,args):
        if args.get('role') == 'student':
            student = Student.objects.filter(uid=args.get('uid')).first()
            student.password = ''
            serializer = StudentSerializers(student)
        else:
            teacher = Teacher.objects.filter(uid=args.get('uid')).first()
            teacher.password = ''
            serializer = TeacherSerializers(teacher)
        return Response({'code':200,'msg':'获取用户信息成功！','data':serializer.data},status=200)

    @resolve_token
    def put(self,request,args):
        data ={'code': 400}
        if args.get('role') == 'student':
            student = Student.objects.filter(uid=args.get('uid')).first()
            serializers = StudentSerializers(student,data=request.data)
        else:
            teacher = Teacher.objects.filter(uid=args.get('uid')).first()
            serializers = TeacherSerializers(teacher,data=request.data)
        try:
            if serializers.is_valid(raise_exception=True):
                user = serializers.save()
                data['code'] = '200'
                data['msg'] = '修改成功'
                return Response(data,status=200)
            else:
                data['msg'] = '修改失败'
        except Exception as e:
            data['msg'] = '修改失败'
            print(e)
        return Response(data,status=400)


class UserCoursers(APIView):
    @resolve_token
    def get(self,request, args):
        """
        根据教师的id获取教师的课程
        :param request:
        :param args:
        :return: list[courses]
        """
        if args.get('role') == 'teacher':
            uid = args.get('uid')
            print('teacherId:'+str(args.get('uid')))
            courses_list = Course.objects.filter(owner_id=uid)
            serializer = CourseSerializers(courses_list,many=True)
            return Response({'code':200,'msg':'获取课程列表成功！','data':serializer.data},status=200)
        else:
            return Response({'code':400,'msg':'请求无效'},status=400)

