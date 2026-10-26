from django import forms

from .models import Author, Category, Post


class PostForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        required=False,
        label="Категории",
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Post
        fields = ["author", "title", "text"]
        labels = {
            "author": "Автор",
            "title": "Заголовок",
            "text": "Текст",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields["categories"].initial = self.instance.categories.all()