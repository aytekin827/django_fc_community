from django.shortcuts import render, redirect
from .models import Fcuser
from django.contrib.auth.hashers import make_password, check_password
from .forms import LoginForm
# Create your views here.

def home(request):
    user_id = request.session.get('user')
    # print(request.session)
    if user_id:
        fcuser = Fcuser.objects.get(pk=user_id)

    return render(request,'home.html')

def logout(request):
    if request.session.get('user'):
        del(request.session['user'])

    return redirect('/')

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            request.session['user'] = form.user_id
            return redirect('/')
    else:
        form = LoginForm()
    return render(request,'login.html',{'form':form})
 

def register(request):
    # register 페이지에 get방식으로 접근했을 때
    if request.method == 'GET':
        return render(request, 'register.html')
    
    # register 페이지에 Post방식으로 접근했을 때, register.html에서 form이 전달되었을 때 
    elif request.method == 'POST':
        
        # register.html 페이지에서 POST로 들어온 값들을 변수로 지정해준다.
        # get함수를 이용해서 기본값을 지정해준다.
        username = request.POST.get('username_name',None)
        useremail = request.POST.get('username_email',None)
        password = request.POST.get('password_pw',None)
        re_password = request.POST.get('re-password_pw',None)

        res_data = {}

        if not (username and password and re_password and useremail):
            res_data['error'] = '[ERROR] - 모든 값을 입력해주셔야 합니다.'
        elif password != re_password:
            res_data['error'] = '[ERROR] - 비밀번호가 다릅니다.'            
        
        # model에 만들어두었던 클래스를 불러와서 객체를 생성해주고
        else:
            fcuser = Fcuser(
                username = username,
                useremail = useremail,
                password = make_password(password) # make_password : 장고에서 기본적으로 제공하는 비밀번호를 암호화해서 return시켜주는 함수
            )

            fcuser.save() # 저장한다.

        return render(request, 'register.html', res_data)

