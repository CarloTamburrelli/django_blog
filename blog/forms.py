from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Comment

class CommentForm(forms.Form):
	message = forms.CharField(widget=forms.Textarea, label = '')


class SearchPosts(forms.Form):
	content = forms.CharField(strip=True, label='', widget=forms.TextInput(attrs={'placeholder': 'Search'}))
	search_by_user = forms.ModelChoiceField(queryset=User.objects.all())
	post_with_comments = forms.BooleanField()
	def __init__(self, *args, **kwargs):
		super(SearchPosts, self).__init__(*args, **kwargs)
		self.fields['content'].required = False
		self.fields['post_with_comments'].required = False
		self.fields['content'].widget.attrs.update({'class': 'form-control mb-4'})
		self.fields['search_by_user'].required = False
		self.fields['search_by_user'].widget.attrs.update({'class': 'form-control mb-4'})


