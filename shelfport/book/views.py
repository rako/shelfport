import logging

from django.urls import reverse_lazy

from django.shortcuts import render, get_object_or_404
from django.views import generic

from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Book

from .forms import BookCreateForm

logger = logging.getLogger(__name__)

# Create your views here.
class IndexView(generic.TemplateView):
    template_name = "index.html"


class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        # URLに埋め込まれた主キーから、本のデータを1件取得。取得できなかった場合は404エラー
        book = get_object_or_404(Book, pk=self.kwargs['pk'])
        # ログインユーザーと本のデータ作成ユーザーを比較し、異なればraise_exceptionの設定に従う
        return self.request.user == book.user


class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book
    template_name = "book_list.html"
    paginate_by = 10
    
    def get_queryset(self):
        books = Book.objects.filter(user=self.request.user).order_by('-created_at') #ハイフンで降順
        return books


class BookDetailView(LoginRequiredMixin, OnlyYouMixin, generic.DetailView):
    model = Book
    template_name = "book_detail.html"


class BookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Book
    template_name = "book_create.html"
    form_class = BookCreateForm
    success_url = reverse_lazy('book:book_list')
    
    def form_valid(self, form):
        book = form.save(commit=False) #入力データが足りない場合は処理できないようにする。モデルオブジェクトを取得する。
        book.user = self.request.user
        book.save()
        messages.success(self.request, '本を登録しました。')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, '本の登録に失敗しました。')
        return super().form_invalid(form)


class BookUpdateView(LoginRequiredMixin, OnlyYouMixin, generic.UpdateView):
    model = Book
    template_name = "book_update.html"
    form_class = BookCreateForm

    def get_success_url(self):
        return reverse_lazy('book:book_detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        messages.success(self.request, '本を更新しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, '本の更新に失敗しました。')
        return super().form_invalid(form)


class BookDeleteView(LoginRequiredMixin, OnlyYouMixin, generic.DeleteView):
    model = Book
    template_name = "book_delete.html"
    success_url = reverse_lazy('book:book_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, '本を削除しました。')
        return super().delete(request, *args, **kwargs)