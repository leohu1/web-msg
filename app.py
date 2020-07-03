from flask import Flask, request, render_template, redirect, url_for, make_response, session, jsonify, flash
import flask_wtf
from wtforms import SubmitField, TextField, PasswordField
from wtforms.validators import DataRequired
from table import *
from flask_bootstrap import Bootstrap
from redis import Redis
from flask_session import Session
from io import BytesIO
from PIL import Image, ImageFont, ImageDraw, ImageFilter
import random

app = Flask(__name__)
app.secret_key = "aHVxaXdlaSUyMHdlYiUyMHNpZGU="
bootstrap = Bootstrap(app)
app.config['SESSION_TYPE'] = 'redis'  # session存储格式为redis
app.config['SESSION_REDIS'] = Redis(  # redis的服务器参数
    host='127.0.0.1',  # 服务器地址
    port=6379)  # 服务器端口
app.config['SESSION_USE_SIGNER'] = True  # 是否强制加盐，混淆session
app.config['SECRET_KEY'] = "aHVxaXdlaSUyMHdlYiUyMHNpZGU="  # 如果加盐，那么必须设置的安全码，盐
app.config['SESSION_PERMANENT'] = False  # sessons是否长期有效，false，则关闭浏览器，session失效
app.config['PERMANENT_SESSION_LIFETIME'] = 3600
app.config['JSON_AS_ASCII'] = False
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
sess = Session(app)


# session长期有效，则设定session生命周期，整数秒，默认大概不到3小时。


class Form(flask_wtf.FlaskForm):
    text = TextField(label='消息:', validators=[DataRequired(message='不可以发空消息！')])
    submit = SubmitField('提交')


class longinForm(flask_wtf.FlaskForm):
    username = TextField(label='用户名(可以为中文)', validators=[DataRequired(message='用户名不可以为空')])
    vercode = TextField(label='验证码', validators=[DataRequired(message='验证码不可以为空')])
    password = PasswordField(label='密码', validators=[DataRequired(message='密码不可以为空')])
    submit = SubmitField('提交')


class VercCode:
    random_letters = 'abcdefghijklmnopqrstuvwxyz012345789'
    width = 107
    height = 43

    @classmethod
    def generate_vercode(cls):
        # 创建一个新的图像, 设置长宽和背景颜色
        img = Image.new('RGB', (cls.width, cls.height), "#f1f0f0")
        font = ImageFont.truetype('genkaimincho.ttf', 30)
        draw = ImageDraw.Draw(img)
        vercode = ""
        # 生成随机验证码,并将验证码转成图像打印到图像
        for item in range(4):
            code = random.choice(cls.random_letters)
            vercode += code
            draw.text((6 + random.randint(1, 2) + 23 * item, 2), text=code, fill=cls.__random_color(), font=font)
        # 画几条随机线,让验证码看起来更专业
        for x in range(4):
            x1 = random.randint(0, cls.width // 2)
            y1 = random.randint(0, cls.height // 2)
            x2 = random.randint(0, cls.width)
            y2 = random.randint(cls.height // 2, cls.height)
            draw.line(((x1, y1), (x2, y2)), fill=cls.__random_color(), width=2)
        # 加上一层滤波器滤镜
        img = img.filter(ImageFilter.EDGE_ENHANCE)
        return img, vercode

    @classmethod
    def __random_color(cls):
        # 随机生成一个RGB颜色值
        return tuple([random.randint(64, 180) for _ in range(3)])


class CustomProxyFix(object):

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        host = environ.get('HTTP_X_FHOST', '')
        if host:
            environ['HTTP_HOST'] = host
        return self.app(environ, start_response)


@app.route('/', methods=['GET', 'POST'])
def index():
    FormOk = Form()
    user = session.get('username')
    if user is not None and user[1] == request.headers.get('User-Agent'):
        show = user
        admin = userad(user[0])
        if request.method == 'POST' and FormOk.text.data is not None:
            add(user[0], FormOk.text.data)
            FormOk.text.data = ''
            # return render_template('page.html', form=FormOk, data=get(), show=show, admin=admin)
    elif user is None:
        admin = False
        show = None
    return render_template('page.html', form=FormOk, data=get(), show=show, admin=admin)


@app.route('/delete/<int:tab_id>', methods=['GET'])
def delete_note(tab_id):
    delet(tab_id)
    return redirect(url_for('index'))


@app.route('/delete_user/<int:user_id>', methods=['GET'])
def wdelete_user(user_id):
    delet_user(user_id)
    return redirect(url_for('back'))


@app.route('/login', methods=['POST', 'GET'])
def islongin():
    response = make_response()
    response.headers['Cache-Control'] = 'no-cache，no-store，must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    logForm = longinForm()
    if session.get('username') is None:
        if request.method == 'POST':
            user = logForm.username.data
            password = logForm.password.data
            vercode = logForm.vercode.data
            if vercode == session.get('vercode'):
                if AddUser(user, password):
                    session['username'] = [user, request.headers.get('User-Agent')]
                    user = None
                    return redirect(url_for('index'))
                else:
                    return render_template('login.html', form=logForm, tit='注册', pas='login')
            else:
                flash('验证码错误', 'danger')
                return render_template('login.html', form=logForm, tit='注册', pas='login')
    else:
        return render_template('err.html', errs='logd', tit='已登录')
    if request.method == 'GET':
        return render_template('login.html', form=logForm, tit='注册', pas='login')


@app.route('/log', methods=['POST', 'GET'])
def log():
    logForm = longinForm()
    # session['username'] = '胡齐伟'
    if session.get('username') is None:
        if 'POST' == request.method:
            user = logForm.username.data
            password = logForm.password.data
            if check(user, password):

                session['username'] = [user, request.headers.get('User-Agent')]
                return redirect(url_for('index'))
            else:
                flash('无此账户', 'danger')
                return render_template('login.html', form=logForm, tit='登录', pas='log')

    else:
        return render_template('err.html', errs='logd', tit='已登录')
    if request.method == 'GET':
        return render_template('login.html', form=logForm, tit='登录', pas='log')


@app.route('/get')
def getr():
    nget = get()
    send = {}
    for i in nget:
        firsend = {'name': nget[i].name, 'text': nget[i].msg}
        send[i] = firsend
    return jsonify(send)


@app.route('/out')
def out():
    try:
        # TODO: write code...
        session.pop('username', None)
    except:
        pass
    return redirect(url_for('index'))


@app.route("/vercode")
def vercode():
    image, vercode = VercCode.generate_vercode()
    buffer = BytesIO()
    image.save(buffer, "png")
    buffer_str = buffer.getvalue()
    response = make_response(buffer_str)
    response.headers['Content-Type'] = 'image/gif'
    session["vercode"] = vercode
    return response


@app.route('/back')
def back():
    user = session.get('username')
    if user is not None:
        if userad(user[0]) is True and request.headers.get('User-Agent') == user[1]:
            return render_template('back.html', data=get(), show=user, userdata=alluers())
        else:
            flash('请登录管理员账户', 'danger')
        return render_template('back.html', data='', show=user)
    else:
        flash('请登录', 'danger')
        return render_template('back.html', data='', show=user)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(403)
def page_no_see(error):
    return render_template('403.html'), 403


app.wsgi_app = CustomProxyFix(app.wsgi_app)

if __name__ == '__main__':
    app.run(port='8000')
