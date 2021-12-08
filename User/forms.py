from django import forms
from .models import users


class RegisterForm(forms.ModelForm):
    password = forms.CharField(label='password', widget=forms.PasswordInput)
    re_password = forms.CharField(label='re_password', widget=forms.PasswordInput)

    class Meta:
        model = users
        fields = ['email','username', 'gender' ] #이 Models.py 필드에 맞게 자동 html form생성됨.

    def clean_re_password(self):
        cd = self.cleaned_data
        if cd['password'] != cd['re_password']:
            raise forms.ValidationError('비밀번호가 일치하지 않습니다.')

        return cd['re_password']