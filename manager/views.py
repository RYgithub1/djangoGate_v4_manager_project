# from django.shortcuts import render
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView

# 問題行テスト用ok?
from django.http import HttpResponse

# ＝＝＝ ログイン認証追加 ＝＝＝
# from django.contrib.auth.views import login
from django.contrib.auth import login
# from django.contrib.auth import login as auth_login
# from django.contrib.auth.views import LoginView
# from django.contrib.auth import views as auth_views

# ＝＝＝ ログアウト ＝＝＝＝＝＝
from django.contrib.auth import logout

# authenticate関数が必要ゆえimport
from django.contrib.auth import authenticate

from manager.models import *


# ＝＝＝ ログイン認証ここでする、のロジックをviewに追加 ＝＝＝
class CustomLoginView(TemplateView):
    template_name = "login.html"

    def get(self, _, *args, **kwargs):
        # if self.request.user.is_authenticated():
        if self.request.user.is_authenticated:
            return redirect(self.get_next_redirect_url())
        else:
            kwargs = {'template_name': 'login.html'}
            return login(self.request, *args, **kwargs)
            # return LoginView(self.request, *args, **kwargs)
            # return HttpResponse("ok?")

    def post(self, _, *args, **kwargs):
        username = self.request.POST['username']
        password = self.request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            # LoginView(self.request, user)
            return redirect(self.get_next_redirect_url())
        else:
            kwargs = {'template_name': 'login.html'}
            return login(self.request, *args, **kwargs)
            # return LoginView(self.request, *args, **kwargs)

    def get_next_redirect_url(self):
        redirect_url = self.request.GET.get('next')
        if not redirect_url or redirect_url == '/':
            redirect_url = '/worker_list/'
        return redirect_url


# 通常の表示
class WorkerListView(TemplateView):
    template_name = "worker_list.html"

    def get(self, request, *args, **kwargs):
        context = super(WorkerListView, self).get_context_data(**kwargs)

        # DBデータの取得
        # データベースからWokerモデルに紐づくオブジェクトをすべて取得して
        # workers = Worker.objects.all()
        # 一部を取得したい場合、filter()で条件指定
        # Person.MANのように、別のクラスの定数を参照する時はクラス名をつける必要
        # workers = Worker.objects.filter(person__sex=Person.MAN)
        # toolbar重い。クエリn1、を解消するため下記
        workers = Worker.objects.all().select_related('person')

        # contextに入れる
        # htmlファイルの中でworkersという変数が有効
        context['workers'] = workers

        return render(self.request, self.template_name, context)


# ＝＝＝＝＝ ログアウト ＝＝ー＝

def logout_view(request):
    logout(request)
    return redirect('/login/')
