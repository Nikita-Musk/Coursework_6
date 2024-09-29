from django.forms import ModelForm

from blog.models import Blog
from mailing_service.forms import StyleFormMixin


class BlogForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Blog
        exclude = ['view_counter']