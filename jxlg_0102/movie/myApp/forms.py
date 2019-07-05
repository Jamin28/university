from .models import User,Text
from django import forms

class RegisterForm(forms.ModelForm):
    password2 = forms.CharField(required=True,min_length=6,error_messages={'required':'必须填写确认密码'})
    class Meta:
        model = User
        fields = '__all__'

class LoginForm(forms.ModelForm):
    def get_errors(self):
        new_errors = []
        errors = self.errors.get_json_data()
        for messages in errors.values():
            for message_dict in messages:
                for key,message in message_dict.items():
                    if key == "message":
                        new_errors.append(message)
        return new_errors

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名不存在')
        return username

    class Meta:
        model = User
        fields = ['username','password1']

        error_messages = {
            'username': {
                'min_length': '用户名至少为6位数'
            },
            'password1': {
                'min_length': '密码至少为6位数'
            }

        }

class TextForm(forms.ModelForm):
    class Meta:
        model = Text
        fields = '__all__'