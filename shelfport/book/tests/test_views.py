from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy

from ..models import Book

class LoggedInTestCase(TestCase):
    """各テストクラスで共通の事前準備処理をオーバーライドした独自TestCaseクラス"""

    def setUp(self):
        """テストメソッド実行前の事前設定"""

        # テストユーザーのパスワード
        self.password = 'pass'

        # 各インスタンスメソッドで使うテスト用ユーザーを生成し
        # インスタンス変数に格納しておく
        self.test_user = get_user_model().objects.create_user(
            username='test_user',
            email='test@test.com',
            password=self.password
        )

        # テスト用ユーザーでログインする
        self.client.login(email=self.test_user.email, password=self.password)

class TestBookCreateView(LoggedInTestCase):
    """BookCreateView用のテストクラス"""

    def test_create_book_success(self):
        """本の新規作成処理が成功することを検証するテストメソッド"""

        # POSTパラメータ
        params = {
            'title': 'テストタイトル',
            'isbn': 1234567890123,
            'content': 'テスト概要',
            'image': '',
            'refer': 'テスト参考文献',
            'refer_url': 'https://test.com',
        }

        # 新規登録処理(post)を実行
        response = self.client.post(reverse_lazy('book:book_create'), params)

        # 本一覧ページへのリダイレクトを検証
        self.assertRedirects(response, reverse_lazy('book:book_list'))

        # 本がデータベースに登録されたかを検証
        self.assertEqual(Book.objects.filter(title='test title').count(), 1)
    
    def test_create_book_failure(self):
        """本の新規作成処理が失敗することを検証するテストメソッド"""

        # 新規登録処理(post)を実行
        response = self.client.post(reverse_lazy('book:book_create'))

        # 必須フォームフィールドが未入力によりエラーになることを検証
        self.assertFormError(response, 'form', 'title', 'このフィールドは必須です。')

class TestBookUpdateView(LoggedInTestCase):
    """BookUpdateView用のテストクラス"""

    def test_update_book_success(self):
        """本の更新処理が成功することを検証するテストメソッド"""

        # 本データの作成
        book = Book.objects.create(
            user=self.test_user,
            title='タイトル編集前',
        )

        # POSTパラメータ
        params = {
            'title': 'タイトル編集後',
        }

        # 更新処理(post)を実行
        response = self.client.post(reverse_lazy('book:book_update', kwargs={'pk': book.pk}), params)

        # 本一覧ページへのリダイレクトを検証
        self.assertRedirects(response, reverse_lazy('book:book_list', kwargs={'pk': book.pk}))

        # 本が更新されたかを検証
        self.assertEqual(Book.objects.get(pk=book.pk).title, '更新タイトル')

    def test_update_book_failure(self):
        """本の更新処理が失敗することを検証するテストメソッド"""

        # 更新処理(post)を実行
        response = self.client.post(reverse_lazy('book:book_update', kwargs={'pk': 9999}))

        # 存在しない本のデータを編集しようとしてエラーになることを検証
        self.assertFormError(response.status_code, 404)

class TestBookDeleteView(LoggedInTestCase):
    """BookDeleteView用のテストクラス"""

    def test_delete_book_success(self):
        """本の削除処理が成功することを検証するテストメソッド"""

        # テスト本データの作成
        book = Book.objects.create(
            user=self.test_user,
            title='削除対象タイトル',
        )

        # 削除処理(post)を実行
        response = self.client.post(reverse_lazy('book:book_delete', kwargs={'pk': book.pk}))

        # 本一覧ページへのリダイレクトを検証
        self.assertRedirects(response, reverse_lazy('book:book_list'))

        # 本が削除されたかを検証
        self.assertEqual(Book.objects.filter(pk=book.pk).count(), 0)

    def test_delete_book_failure(self):
        """本の削除処理が失敗することを検証するテストメソッド"""

        # 削除処理(post)を実行
        response = self.client.post(reverse_lazy('book:book_delete', kwargs={'pk': 9999}))

        # 存在しない本のデータを削除しようとしてエラーになることを検証
        self.assertEqual(response.status_code, 404)