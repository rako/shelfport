from .models import Book

from django import forms

class BookCreateForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'isbn', 'content', 'image', 'refer', 'refer_url')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values(): #Bootstrapのクラスを追加
            field.widget.attrs['class'] = 'form-control'