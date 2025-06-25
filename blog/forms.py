from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["name", "email", "content"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "نام شما"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "ایمیل شما"}
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "متن کامنت شما...",
                }
            ),
        }
        labels = {
            "name": "نام",
            "email": "ایمیل",
            "content": "متن کامنت",
        }


class SearchForm(forms.Form):
    q = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "جستجو در پست‌ها..."}
        ),
    )
