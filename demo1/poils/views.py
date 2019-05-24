from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login as lgi, logout as lgo
from .models import Questions, Choices, MyUser
from django.core.mail import send_mail, send_mass_mail, EmailMultiAlternatives
from django.conf import settings
from PIL import Image,ImageDraw,ImageFont
import random,io
from django.views.generic import View
# 引入序列化加密并且有效期信息
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer,SignatureExpired
# Create your views here.


def login(request):
    if request.method == 'GET':
        return render(request, 'poils/login.html')
    else:
        username = request.POST.get('username')
        pwd = request.POST.get('password')
        # 第一种，不用激活直接进入
        # user = authenticate(request, username=username, password=pwd)
        # if user:
        #     lgi(request, user)
        #     return redirect(reverse('poils:index'))
        # else:
        #     return render(request, 'poils/login.html')

        verifycode = request.POST["verify"]
        # 判断验证码是否输入正确
        if verifycode == request.session["verifycode"]:
            # 第二种： 判断用户是否激活
            user = get_object_or_404(MyUser, username=username)
            if not user.is_active:
                error = '用户尚未激活'
                return render(request, 'poils/login.html', locals())
            else:
                check = user.check_password(pwd)
                if check:
                    lgi(request, user)
                    return redirect(reverse('poils:index'))
                else:
                    return render(request, 'poils/login.html', {'error':'用户名或者密码错误'})
        else:
            return render(request, 'poils/login.html', {"error": "验证码错误"})


def loginout(request):
    lgo(request)
    return redirect(reverse('poils:login'))


def register(request):
    if request.method == 'GET':
        return render(request, reverse('poils/login.html'))
    elif request.method == 'POST':
        username = request.POST.get('manage')
        pwd = request.POST.get('password1')
        pwd2 = request.POST.get('password2')
        email = request.POST.get('email')
        print(username, pwd,)
        error = None
        if MyUser.objects.filter(username=username):
            error = '用户已存在'
            return render(request, 'poils/login.html', locals())
        else:
            if pwd != pwd2:
                error = '两次密码输入不一致'
                return render(request, 'poils/login.html', {'error': error})
            else:
                user = MyUser.objects.create_user(username=username, password=pwd, phone='15555', is_active=False)

                # 第二种 注册后需要进入邮箱进行激活才能进入系统
                # user.is_active = False
                # user.save()
                # 为了防止非人为激活，需要将激活地址加密
                # 带有有效期的序列化
                # 1 得到序列化工具
                serutil = Serializer(settings.SECRET_KEY)
                # 2 使用工具对字典对象序列化
                result = serutil.dumps({"userid": user.id}).decode("utf-8")

                msg = EmailMultiAlternatives("点击激活用户", "<a href='http://127.0.0.1:8000/poils/authen/%s/'>点击激活</a>" % result,
                                             settings.DEFAULT_FROM_EMAIL, [email])
                msg.content_subtype = "html"
                msg.send()

                return render(request, 'poils/login.html', {"error": "请在一个小时之内激活"})

# 激活用户
def authen(request, info):
    serutil = Serializer(settings.SECRET_KEY)
    try:
        obj = serutil.loads(info)
        id = obj["userid"]

        user = get_object_or_404(MyUser, pk=id)
        user.is_active = True
        user.save()
        error = '已经激活，请登录'
        return render(request, 'poils/login.html', locals())
        # return redirect(reverse('poils:login', locals()))
    except SignatureExpired as e:
        return HttpResponse("过期了")

# Ajax 异步刷新
def checkuser(request):
    if request.method == "POST":
        username = request.POST.get("username")
        print(username, '###################')
        if MyUser.objects.filter(username=username).first():
            print(MyUser.objects.filter(username=username).first())
            return JsonResponse({"state": 1})
        else:
            return JsonResponse({"state": 0, "error":"用户不存在"})

# 验证码
def verify(request):
    bgcolor = (random.randrange(20, 100),
               random.randrange(20, 100),
               random.randrange(20, 100))
    width = 100
    heigth = 35
    # 创建画面对象
    im = Image.new('RGB', (width, heigth), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        # 随机取得位置
        xy = (random.randrange(0, width), random.randrange(0, heigth))
        # 随机取得颜色
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        # 填充
        draw.point(xy, fill=fill)
    # 定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    # 构造字体对象
    font = ImageFont.truetype('FZSTK.TTF', 23)
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    # 释放画笔
    del draw
    request.session['verifycode'] = rand_str
    f = io.BytesIO()
    im.save(f, 'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(f.getvalue(), 'image/png')


def index(request):
    que = Questions.objects.all()

    return render(request, 'poils/index.html', locals())
    # return HttpResponse('首页')


def choice(request, id):
    choice = Questions.objects.get(pk=int(id))
    return render(request,'poils/choice.html',{'ques':choice})
    # return HttpResponse('选择页')

def choicehand(request):
    chid = request.POST['chid']
    qid = request.POST['id']
    print(qid)
    print(chid)

    que = Questions.objects.get(pk=qid)
    ch = Choices.objects.get(pk=chid)
    ch.num += 1
    # ch.cquesid = que
    ch.save()

    return render(request,'poils/choicehand.html',{'que':que})
    # return HttpResponse('h1')

def result(request):
    ch = Choices.objects.all()
    q = Questions.objects.all()

    return render(request,'poils/result.html', {'que':q})
