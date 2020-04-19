import re
from django import forms
from captcha.fields import CaptchaField

from DjangoUeditor.forms import UEditorField

from .models import UserProfile, Province, City, Classes

class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=6, max_length=12)

class RegisterForm(forms.Form):
    username = forms.CharField(required=True,max_length=10)
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=6, max_length=12)
    user_type = forms.CharField(required=True)
    # captcha = CaptchaField(error_messages={'invalid':'验证码错误！'})

class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    # captcha = CaptchaField(error_messages={'invalid':'验证码错误！'})

class ResetForm(forms.Form):
    password = forms.CharField(required=True, min_length=6, max_length=12)
    email = forms.EmailField(required=True)


class ModifyUserForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image', 'username', 'gender', 'birthday', 'mobile', 'province', 'city', 'QQ', 'desc']

    def clean_mobile(self):
        if not self.cleaned_data['mobile']:
            return ''
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError('手机号码非法！', code='mobile_invalid')

    def clean_QQ(self):
        if not self.cleaned_data['QQ']:
            return ''
        QQ = self.cleaned_data['QQ']
        REGEX_QQ = "^[0-9]{5,9}$"
        p = re.compile(REGEX_QQ)
        if p.match(QQ):
            return QQ
        else:
            raise forms.ValidationError('QQ号非法！', code='QQ_invalid')


class ChangePwdForm(forms.Form):
    old_password = forms.CharField(required=True, min_length=6, max_length=12)
    new_password = forms.CharField(required=True, min_length=6, max_length=12)
    re_password = forms.CharField(required=True, min_length=6, max_length=12)
    verify_code = forms.CharField(required=True, min_length=4, max_length=4)


class AddClassForm(forms.Form):
    school = forms.CharField(required=False, max_length=20)
    grade = forms.CharField(required=True, max_length=10)
    class_name = forms.CharField(required=False, max_length=10)


class TutorForm(forms.Form):
    name = forms.CharField(max_length=10, required=True)
    student_gender = forms.CharField(max_length=10, required=True)
    mobile = forms.CharField(max_length=11, required=True)
    address = forms.CharField(max_length=100, required=True)
    grade = forms.CharField(required=True)
    subject = forms.MultipleChoiceField(choices=(('1','语文'),('2','数学'),('3','英语'),('4','历史'),('5','地理'),('6','政治'),('7','生物'),('8','物理'),('9','化学'),('0','其他')), required=True)
    # subject = forms.MultipleChoiceField(required=True)
    student_info = forms.CharField(max_length=500, required=False)
    teacher_gender = forms.CharField(max_length=10, required=True)
    teacher_require = forms.CharField(max_length=500, required=False)
    pay = forms.CharField(max_length=50, required=True)
    captcha = CaptchaField(error_messages={'invalid': '验证码错误！'})

    def clean_mobile(self):
        if not self.cleaned_data['mobile']:
            return ''
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError('手机号码非法！', code='mobile_invalid')


class TestForm(forms.Form):
    test = UEditorField('测试', width=600, height=300, toolbars='mini')