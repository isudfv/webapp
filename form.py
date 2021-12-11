from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FloatField, TextAreaField, FileField, IntegerField, EmailField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    passwd = PasswordField('密码', validators=[DataRequired()])
    # remember_me = BooleanField('保持登录状态')
    submit = SubmitField('登录')


class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    passwd = PasswordField('密码', validators=[DataRequired()])
    repasswd = PasswordField('确认密码', validators=[DataRequired()])
    submit = SubmitField('注册')

class ObjectForm(FlaskForm):
    file_upload = FileField('上传图片', validators=[FileAllowed(['png', 'jpg', 'jpeg'])])
    # img = StringField('商品图片', validators=[DataRequired()])
    # id = IntegerField('商品编号', validators=[DataRequired()])
    name = StringField('商品名称', validators=[DataRequired()])
    description = StringField('商品描述', validators=[DataRequired()])
    # author = StringField('作者', validators=[DataRequired()])
    # isbn = StringField('ISBN', validators=[DataRequired()])
    # press = StringField('出版社', validators=[DataRequired()])
    # fixed_price = FloatField('定价', validators=[DataRequired()])
    price = FloatField('售价', validators=[DataRequired()])
    # wear = FloatField('新旧程度', validators=[DataRequired()])
    submit = SubmitField('添加')

class BuyForm(FlaskForm):
    email = EmailField('邮箱', validators=[DataRequired()])
    submit = SubmitField('购买')