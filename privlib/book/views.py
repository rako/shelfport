from django.shortcuts import render
from django.views import generic

from .forms import InquiryForm

# Create your views here.
class IndexView(generic.TemplateView):
    template_name = 'index.html' #テンプレートの表示に特化したビュークラスのクラス変数（template_name）を設定、アプリ用ディレクトリ内のtemplatesディレクトリ内から探す

class InquiryView(generic.FormView):
    template_name = "inqiry.html"
    form_class = InquiryForm