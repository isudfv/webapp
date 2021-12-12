import os
from flask import Flask, render_template, flash, redirect, url_for, session, request
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename

from form import *
from user import *
from goods import *

app = Flask(__name__, static_url_path='/static')
app.debug = True
app.secret_key = os.getenv('SECRET_KEY', '1234')
bootstrap = Bootstrap(app=app)

app.config["MAIL_SERVER"] = "smtp.qq.com"
app.config["MAIL_PORT"] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config["MAIL_USERNAME"] = "yieatn@qq.com"
app.config["MAIL_PASSWORD"] = "nkthhsmzyrtcgehd"
mail = Mail(app)

login_manager = LoginManager()
# login_manager.login_view = 'login'
# login_manager.login_message_category = 'info'
# login_manager.login_message = 'Access denied.'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_name):
    return User.get(user_name)


@app.route('/')
def hello_world():  # put application's code here
    return redirect(url_for('login'))
    # return render_template('login.html', test=123)


@app.route('/login', methods=["POST", "GET"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        username = login_form.username.data
        passwd = login_form.passwd.data
        # 从数据库查询用户
        if findUser(username):
            user = User(username)
        else:
            flash("用户不存在")
            return redirect(url_for('login'))
        if passwd != user.passwd:
            flash('密码错误')
            return redirect(url_for('login'))
        # 用flask-login管理用户登录
        login_user(user)

        return redirect(url_for('commodity'))
    return render_template('login.html', form=login_form)


@app.route('/register', methods=["POST", "GET"])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        username = register_form.username.data
        passwd = register_form.passwd.data
        repasswd = register_form.repasswd.data

        # 从数据库查询用户
        if findUser(username):
            flash('用户已存在')
            return redirect(url_for('register'))
        if passwd != repasswd:
            flash('密码不一致')
            return redirect(url_for('register'))

        addUser(username, passwd)
        session['trolley'] = []
        session['bought'] = []
        flash("注册成功")
        return redirect(url_for('login'))
    return render_template('register.html', form=register_form)


@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/commodity', methods=['GET', 'POST'])
def commodity():
    commodity_list = getAllGoodsOnSale()
    add_commodity_form = ObjectForm()
    if add_commodity_form.validate_on_submit():
        filename = add_commodity_form.file_upload.data.filename
        # 保存路径为/static/image
        path = os.path.join('static', 'image', filename)
        add_commodity_form.file_upload.data.save(path)
        # 向数据库中添加数据
        addGoods(add_commodity_form.name.data, add_commodity_form.description.data, add_commodity_form.price.data, filename)
        return redirect(url_for('commodity'))
    return render_template('commodity.html', form_list=commodity_list, form=add_commodity_form)


@app.route('/add/<int:id>', methods=['GET'])
@login_required
def add(id):
    # print(type(session['trolley']))
    List = session.get('trolley')
    if List is None:
        session['trolley'] = []
        List = []
    List.append(getGoodsById(id))
    session['trolley'] = List
    # print(id)
    print(List)
    return redirect(url_for('commodity'))


@app.route('/remove/<int:id>', methods=['GET'])
@login_required
def remove(id):
    # print(type(session['trolley']))
    List = session.get('trolley')
    # if List is None:
    #     session['trolley'] = []
    #     List = []
    del List[id]
    session['trolley'] = List
    # print(id)
    print(List)
    return redirect(url_for('my_trolley'))


@app.route('/trolley', methods=['GET'])
@login_required
def my_trolley():
    # print(type(session['trolley']))
    # session['trolley'].append(id)
    # print(session['trolley'])
    List = session.get('trolley')
    if List is None:
        session['trolley'] = []
    tot = 0
    for i in session['trolley']:
        tot += i['price']
    return render_template('trolley.html', list=session.get('trolley'), tot=tot)


@app.route('/buy', methods=['GET', 'POST'])
@login_required
def buy():
    buy_form = BuyForm()
    if buy_form.validate_on_submit():
        bought = session.get('bought')
        if bought is None:
            session['bought'] = []
            bought = []
        # 清空购物车, 添加购买记录
        this_buy = session['trolley']
        bought += this_buy
        session['trolley'] = []
        session['bought'] = bought
        # 发送邮件
        user_email = buy_form.email.data
        message = Message("您已购买", sender=app.config["MAIL_USERNAME"], recipients=[user_email])
        message.body = '\n'.join([f"商品: {v['name']}"for v in this_buy])
        # print()
        flash("购买成功")
        mail.send(message)
        return redirect(url_for('commodity'))
    return render_template('buy.html', form=buy_form)


@app.route('/history', methods=['GET'])
@login_required
def history():
    bought = session.get('bought')
    if bought is None:
        session['bought'] = []
    return render_template('history.html', list=session.get('bought'))


@app.route('/del/<int:id>', methods=['GET'])
@login_required
def delete(id):
    # print(type(session['trolley']))
    rmGoodsById(id)
    return redirect(url_for('commodity'))


# @app.route('/manage', methods=['GET', 'POST'])
# @login_required
# def history():
#     return render_template('manage.html', list=session.get('bought'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
