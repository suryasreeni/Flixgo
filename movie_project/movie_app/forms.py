from django import forms
from .models import products
from .models import Comment, Rating
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model



class ProductForm(forms.ModelForm):
    class Meta:
        model = products
        fields = ['name', 'poster', 'description', 'release_date', 'actors', 'category_id', 'trailer_link']
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ['username','first_name','last_name','email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password')
