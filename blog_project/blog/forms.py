
from django import forms
from .models import Comment
import re
from django.core.exceptions import ValidationError
from django.core.cache import cache


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

    def clean_text(self):
        text = self.cleaned_data['text']

        # запрет HTML
        if re.search(r'<.*?>', text):
            raise ValidationError('HTML tags are not allowed')

        if len(text) > 500:
            raise ValidationError('Maximum 500 characters')

        return text

