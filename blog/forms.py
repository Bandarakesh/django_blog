from django import forms
from .models import CustomUser, School
from django import forms
from .models import Comment
from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content'] 

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data['email']
        domain = email.split('@')[-1]
        print(f"Email: {email}, Domain: {domain}")
        if not School.objects.filter(domain=domain).exists():
            print(f"No School found for domain: {domain}")
            raise forms.ValidationError("Please register using your school email address.")
        return email

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']