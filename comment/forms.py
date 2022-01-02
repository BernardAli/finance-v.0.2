from django import forms
from comment.models import Comment


class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'cols': '80'}), required=True)
    author = forms.CharField(widget=forms.TextInput(), required=True)

    class Meta:
        model = Comment
        fields = ('body', 'author')
