import hashlib
import os
import uuid

from django.http import JsonResponse
from django.shortcuts import render,redirect,reverse

from AXF.settings import MEDIA_ROOT, BASE_DIR
from .models import *

def home(request):
    # 轮播数据
    wheels = MainWheel.objects.all()
    # 导航数据
    navs = MainNav.objects.all()
    # 必购数据
    mustbuys = MainMustbuy.objects.all()
    # shop数据
    shops = MainShop.objects.all()
    shop0 = shops.first()
    shop1_2 = shops[1:3]
    shop3_6 = shops[3:7]
    shop7_10 = shops[7:11]
    mainshows = MainShow.objects.all()

    data = {
        'wheels':wheels,
        'navs':navs,
        'mustbuys':mustbuys,
        'shop0': shop0,
        'shop1_2': shop1_2,
        'shop3_6': shop3_6,
        'shop7_10': shop7_10,
        'mainshows': mainshows,
    }
    return render(request,'home/home.html',data)

def market(request):
    return redirect(reverse('App:market_with_params', args=['104749', '0', '0']))

# 带参数的闪购
def market_with_params(request, typeid, typechildid, sortid):

    # 分类数据
    foodtypes = FoodType.objects.all()
    # 商品数据,根据主分类id进行筛选
    goods_list = Goods.objects.filter(categoryid=typeid)

    # 再按照子分类进行筛选
    if typechildid != '0':
        goods_list = goods_list.filter(childcid=typechildid)

    # 获取当前主分类下的所有子分类
    childnames = FoodType.objects.filter(typeid=typeid)
    # '全部分类:0#进口水果:103534#国产水果:103533'

    child_type_list = []  # 存放子分类的数据
    if childnames.exists():
        childtypes = childnames.first().childtypenames.split('#')
        # print(childtypes)  # ['全部分类:0', '进口水果:103534', '国产水果:103533']

        for type in childtypes:
            type_list = type.split(':')  # ['进口水果', '103534']
            child_type_list.append(type_list)

    # print(child_type_list)
    # [['全部分类', '0'], ['进口水果', '103534'], ['国产水果', '103533']]

    # 排序规则
    if sortid == '0':  # 综合排序
        pass
    elif sortid == '1':  # 销量排序
        goods_list = goods_list.order_by('-productnum')
    elif sortid == '2':  # 价格降序
        goods_list = goods_list.order_by('-price')
    elif sortid == '3':  # 价格升序
        goods_list = goods_list.order_by('price')

    data = {
        'foodtypes': foodtypes,
        'goods_list': goods_list,
        'typeid': typeid,
        'child_type_list': child_type_list,
        'typechildid': typechildid,
    }

    return render(request, 'market/market.html', data)




# 加入购物车
def add_to_cart(request):
    data = {
        'status': 1,
        'msg': 'ok',
    }

    # 判断用户是否登录了
    userid = request.session.get('userid', '')
    if not userid:
        data['status'] = 0
        data['msg'] = '未登录'

    else:
        # 如果登录了
        if request.method == 'GET':
            goodsid = request.GET.get('goodsid')
            num = request.GET.get('num')
            print(goodsid,num)

            # 添加到购物车
            cart = Cart()
            cart.user_id = userid
            cart.goods_id = goodsid
            cart.num = num
            cart.save()

        else:
            data['status'] = -1
            data['msg'] = '请求方式不正确'

    return JsonResponse(data)

def mine(request):
    data = {
        'name': '',
        'icon': ''
    }

    # 获取session
    userid = request.session.get('userid', "")

    if userid:
        user = User.objects.get(id=userid)
        name = user.name  # 用户名
        icon = user.icon  # 头像名称
        data['name'] = name
        # print("icon:", icon)
        data['icon'] = '/upload/icon/' + icon

    return render(request,'mine/mine.html', data)

def register(request):
    return render(request,'user/register.html')

def register_handle(request):
    data = {
        'status': 1,
        'msg': 'ok',
    }

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        icon = request.FILES.get('icon', "")

        # 注册
        try:

            user = User()
            user.name = username
            user.password = password
            user.email = email
            user.icon = icon
            user.save()


            # 头像
            if icon:

                filename = random_file() + '.png'  # icon.name

                user.icon = filename

                filepath = os.path.join(MEDIA_ROOT, filename)
                with open(filepath, 'ab') as fp:
                    for part in icon.chunks():
                        fp.write(part)
                        fp.flush()

            else:
                user.icon = ""
            user.save()

            # 保存session
            request.session['userid'] = user.id

            return redirect(reverse('App:mine'))

        except:
            return redirect(reverse('App:register'))

    return redirect(reverse('App:register'))

# 获取随机的文件名称
def random_file():
    u = str(uuid.uuid4())
    m = hashlib.md5()
    m.update(u.encode('utf-8'))
    return m.hexdigest()

def check_username(request):

    if request.method == 'GET':
        username = request.GET.get('username')

        # 检测用户名是否存在
        users = User.objects.filter(name=username)

        # 如果存在
        if users.exists():
            return JsonResponse({'status': 0, 'msg': '用户名已经存在'})
        # 如果不存在
        else:
            return JsonResponse({'status': 1, 'msg': 'ok'})

    return JsonResponse({'status': -1, 'msg': '请求方式错误'})

def login(request):
    return render(request, 'user/login.html')

# 登录操作
def login_handle(request):
    data = {
        'status': 1,
        'msg': 'ok',
    }
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 匹配用户名和密码
        users = User.objects.filter(name=username, password=password)
        if users.exists():
            # 如果登录成功，则进入‘我的’页面
            request.session['userid'] = users.first().id  # 保存session
            return redirect(reverse('App:mine'))
        else:
            data['status'] = 0
            data['msg'] = '用户名或密码错误'
            return render(request, 'user/login.html', data)

    data['status'] = -1
    data['msg'] = '请求方式不正确'
    return render(request, 'user/login.html', data)

# 退出登录
def logout(request):
    # 删除session
    request.session.flush()
    return redirect(reverse('App:mine'))

def cart(request):

    userid = request.session.get('userid', '')
    if not userid:
        return redirect(reverse('App:login'))
    else:
        carts = Cart.objects.filter(user_id=userid)
        return render(request, 'cart/cart.html', {'carts': carts})

def add_num(request):
    data = {
        'status': 1,
        'msg': 'ok',
    }

    userid = request.session.get('userid', '')
    if not userid:
        data['status'] = 0
        data['msg'] = '未登录'
    else:
        # 如果登录了
        if request.method == 'GET':
            cartid = request.GET.get('cartid')

            # 数量+1
            cart = Cart.objects.get(id=cartid)
            cart.num = cart.num + 1
            cart.save()
            data['num'] = cart.num

        else:
            data['status'] = -1
            data['msg'] = '请求方式不正确'

    return JsonResponse(data)

def reduce_num(request):
    data = {
        'status': 1,
        'msg': 'ok',
    }

    userid = request.session.get('userid', '')
    if not userid:
        data['status'] = 0
        data['msg'] = '未登录'
    else:
        # 如果登录了
        if request.method == 'GET':
            cartid = request.GET.get('cartid')

            # 数量-1
            cart = Cart.objects.get(id=cartid)
            cart.num = cart.num - 1
            if cart.num < 1:
                cart.num = 1
            cart.save()
            data['num'] = cart.num

        else:
            data['status'] = -1
            data['msg'] = '请求方式不正确'

    return JsonResponse(data)
def delete_cart(request):
    data = {
        'status': 1,
        'msg': 'ok',
    }
    userid = request.session.get('userid', '')
    if not userid:
        data['status'] = 0
        data['msg'] = '未登录'
    else:
        if request.method == "GET":
            cartid = request.GET.get('cartid')

            # 删除
            Cart.objects.filter(id=cartid).delete()
        else:
            data['status'] = -1
            data['msg'] = '请求方式不正确'

    return JsonResponse(data)

def cart_select(request):
    data = {
        'status': 1,
        'msg': 'ok',
    }
    userid = request.session.get('userid', '')
    if not userid:
        data['status'] = 0
        data['msg'] = '未登录'
    else:
        if request.method == "GET":
            cartid = request.GET.get('cartid')
            # 勾选/取消勾选
            cart = Cart.objects.get(id=cartid)
            cart.is_select = not cart.is_select
            cart.save()
            data['is_select1'] = cart.is_select

        else:
            data['status'] = -1
            data['msg'] = '请求方式不正确'

    return JsonResponse(data)

def cart_selectall(request):
    data = {
        'status': 1,
        'msg': 'ok',
    }
    userid = request.session.get('userid', '')
    if not userid:
        data['status'] = 0
        data['msg'] = '未登录'
    else:
        if request.method == "GET":
            action = request.GET.get('action')
            selects = request.GET.get('selects')
            select_list = selects.split('#')  # [10, 13, 14]
            # print(action, selects)  # cancelselect 10#13#14

            # 全不选
            if action == 'cancelselect':
                Cart.objects.filter(id__in=select_list).update(is_select=False)
            # 全选
            else:
                Cart.objects.filter(id__in=select_list).update(is_select=True)

        else:
            data['status'] = -1
            data['msg'] = '请求方式不正确'

    return JsonResponse(data)