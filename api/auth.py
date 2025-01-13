from flask import Blueprint, g
from flask_wtf import FlaskForm

from werkzeug.security import check_password_hash
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length
from model.connent import db
from api import resp
from model.tables import User, UserRole
from api.middleware import generate_token, generate_refresh_token, verify_refresh_token

# 创建一个 Blueprint，命名为 user
auth_api = Blueprint('auth', __name__)


class LoginForm(FlaskForm):
    userName = StringField('userName', validators=[DataRequired(), Length(min=1, max=80)])
    password = PasswordField('password', validators=[DataRequired(), Length(min=6)])


@auth_api.route('/login', methods=['POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit() is False:
        return resp.err(form.errors)
    userName = form.userName.data
    password = form.password.data

    # 查询用户
    u = User.query.filter_by(userName=userName).first()

    if (u is not None and check_password_hash(u.password, password)) is False:
        return resp.err('Invalid username or password')

    return resp.succ(data={
        "token": generate_token(u.id),
        "refreshToken": generate_refresh_token(u.id)
    })


class refreshTokenForm(FlaskForm):
    refreshToken = StringField('refreshToken', validators=[DataRequired(), Length(min=1, max=120)])


@auth_api.route('/refreshToken', methods=['POST'])
def refreshToken():
    form = refreshTokenForm()
    if form.validate_on_submit() is False:
        return resp.err(form.errors)

    payload = verify_refresh_token(form.refreshToken.data)
    if payload is None:  # 假设 'valid_token' 是有效的 token
        return resp.err('Invalid token')

    return resp.succ(data={
        "token": generate_token(payload['uid']),
        "refreshToken": generate_refresh_token(payload['uid'])
    })


@auth_api.route('/getUserInfo', methods=['GET'])
def getUserInfo():
    uid = g.uid
    u = User.query.filter_by(id=uid).first()

    ul = db.session.query(UserRole.roleCode).filter(UserRole.userId == uid).all()
    return resp.succ(data={
        "userId": u.id,
        "userName": u.userName,
        "roles": [item[0] for item in ul],
        "buttons": []
    })
