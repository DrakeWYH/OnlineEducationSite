from random import Random
from django.core.mail import send_mail
from users.models import EmailVerifyRecord
from OnlineEducationSite.settings import EMAIL_FROM


def random_str(randomlength = 8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars)-1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


def send_user_email(email, send_type='register'):
    email_record = EmailVerifyRecord()
    if send_type == 'change':
        code = random_str(4)
    else:
        code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.is_valid = True
    email_record.save()

    email_title = ''
    email_body = ''

    if send_type == 'register':
        email_title = '在线教育网站注册用户激活链接'
        email_body = '请点击下面链接激活用户：http://202.116.39.8:8080/active/{0}'.format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        return send_status

    elif send_type == 'forget':
        email_title = '在线教育网站重置密码链接'
        email_body = '请点击下面链接重置密码：http://202.116.39.8:8080/reset/{0}'.format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        return send_status

    elif send_type == 'change':
        email_title = '在线教育网站修改密码验证码'
        email_body = '请在密码修改页面输入以下验证码：{0}'.format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        return send_status

    else:
        return 0

