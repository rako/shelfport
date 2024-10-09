from django.urls import path

from . import views

#ビューでリダイレクトさせたり、テンプレート内でURLを逆引きする際に使うから、
#他のアプリケーションと名前が被らないようにするために、アプリケーションごとに名前をつける
app_name = 'book'

#「name=」では、アプリケーション用urls.py内で名前の衝突を避けるため
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
]