from django.shortcuts import render
from django.views import generic

from .forms import InquiryForm

import logging

from djang.urls import reverse_lazy

logger = logging.getLogger(__name__)

# Create your views here.
class IndexView(generic.TemplateView):
    template_name = 'index.html' #テンプレートの表示に特化したビュークラスのクラス変数（template_name）を設定、アプリ用ディレクトリ内のtemplatesディレクトリ内から探す

class InquiryView(generic.FormView):
    template_name = "inquiry.html"
    form_class = InquiryForm
    success_url = reverse_lazy('book:inquiry') #reverse_lazy関数を使って、URLパターンの名前を指定している。ハードコーディングを避けるため。

    def form_valid(self, form):
        form.send_email()
        logger.info('Inquiry sent by {}'.format(form.cleaned_data['name']))
        return super().form_valid(form)