from rest_framework.views import APIView
from rest_framework.response import Response
from user.models import *
from user.serializers import StudentSerializers, TeacherSerializers
from .login_token import *
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


class LoginView(APIView):
    #permission_classes = [] # 取消全局token认证

    def post(self,request):
        """
        用户登录验证视图函数
        :param request: 提交的form 请求
        :return: 登录验证情况
        """
        data = {'code':401}
        print(request.data)
        req = request.data
        if req.get('role') == 'student':
            # 学生登录验证
            role = 'student'
            student = Student.objects.filter(username=req.get('username')).first()
            if student:
                if check_password(req.get('password'), student.password):
                    data['code'] = 200
                    data['msg'] = 'login successful'
                    data['token'] = create_token(student, role)
                    return Response(data,status=200)
                else:
                    data['msg'] = 'password  is wrong'
                    return Response(data,status=401)
            else:
                data['msg'] = 'no user named'+req.get('username')
                return Response(data,status=401)
        else:
            # 教师登录验证
            role = 'teacher'
            teacher = Teacher.objects.filter(username=req.get('username')).first()
            if teacher:
                if check_password(req.get('password'), teacher.password):
                    data['code'] = 200
                    data['msg'] = 'login success'
                    data['token'] = create_token(teacher, role)
                    return Response(data, status=200)
                else:
                    data['msg'] = 'password  is wrong'
                    return Response(data, status=401)
            else:
                data['msg'] = 'no user named' + req.get('username')
                return Response(data, status=401)


class RegisterView(APIView):
    permission_classes = []  # 取消全局token认证

    def post(self,request):
        data ={'code':400}
        print(request.data)
        if request.data.get('role') == 'student':
            serializers = StudentSerializers(data=request.data)
        else:
            serializers = TeacherSerializers(data=request.data)
        try:
            if serializers.is_valid():
                user = serializers.save()
                data['code'] = 201
                data['msg'] = ''
                # role = serializers.validated_data.get('role')
                # data['token'] = create_token(user, role)
                return Response(data, status=201)
            else:
                data['msg'] = '用户名已存在！'
                return Response(data, status=401)
        except Exception as e:
            print(e)
            data['msg'] = '密码不能为空'
        return Response(data,status=401)


class JWTview(APIView):
    # permission_classes =[Authenticated] # 使用自定义类的校验方法
    @resolve_token
    def get(self,request,args):
        print(args)
        if args.get('role') == 'student':
            print('student')
            student = Student.objects.get(uid=args.get('uid'))
            serializer = StudentSerializers(student)
        else:
            print('teacher')
            teacher = Teacher.objects.get(uid=args.get('uid'))
            serializer = TeacherSerializers(teacher)
        return Response({'code': 200, 'msg': 'token校验成功', 'user': serializer.data})




