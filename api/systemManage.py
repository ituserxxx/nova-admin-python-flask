from flask import Blueprint, request
from datetime import datetime
from werkzeug.security import generate_password_hash
from model.connent import db
from sqlalchemy.exc import IntegrityError
from api import resp
from model.tables import User, Role, UserRole
from flask_wtf import FlaskForm

from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Length

# 创建一个 Blueprint，命名为 user
systemManage_api = Blueprint('systemManage', __name__)


@systemManage_api.route('/getAllRoles', methods=['GET'])
def getAllRoles():
    ul = db.session.query(Role).with_entities(Role.id, Role.roleName, Role.roleCode).all()
    ul_dict = [{"id": item[0], "roleName": item[1], "roleCode": item[2]} for item in ul]
    return resp.succ(data=ul_dict)


@systemManage_api.route('/getRoleList', methods=['GET'])
def getRoleList():
    # 获取 GET 请求中的参数，若没有提供，则使用默认值
    current = request.args.get('current', default=1, type=int)
    size = request.args.get('size', default=10, type=int)
    status = request.args.get('status', default=None, type=int)
    roleName = request.args.get('roleName', type=str)
    roleCode = request.args.get('roleCode', type=str)
    # 初始化查询
    query = db.session.query(Role)

    # 根据 status 过滤
    if status is not None:
        query = query.filter(Role.status == status)

    # 根据 roleName 过滤
    if roleName:
        query = query.filter(Role.roleName == roleName)
        # query = query.filter(Role.roleName.like(f"%{roleName}%"))

    # 根据 roleCode 过滤
    if roleCode:
        query = query.filter(Role.roleCode == roleCode)
        # query = query.filter(Role.roleCode.like(f"%{roleCode}%"))

    # 获取总数
    total_count = query.count()

    # 分页处理
    ul = query.offset((current - 1) * size).limit(size).all()

    return resp.succ(data={
        "records": [item.to_dict() for item in ul],
        "current": current,
        "size": size,
        "total": total_count
    })


class roleAddForm(FlaskForm):
    roleCode = StringField('roleCode', validators=[DataRequired(), Length(min=1, max=50)])
    roleName = StringField('roleName', validators=[DataRequired(), Length(min=1, max=30)])
    roleDesc = StringField('roleDesc')
    status = IntegerField('status', validators=[DataRequired()])


@systemManage_api.route('/roleAdd', methods=['POST'])
def roleAdd():
    form = roleAddForm()
    if form.validate_on_submit() is False:
        return resp.err(form.errors)
    # 判断角色编码存在
    existing_roleCode = Role.query.filter_by(roleCode=form.roleCode.data).first()

    if existing_roleCode:
        # 如果角色编码已存在，返回错误信息
        return resp.succ(data="角色编码已存在")

    # 用户名不存在，进行新增操作
    new_role = Role(
        createBy="super",
        createTime=datetime.utcnow(),
        roleName=form.roleName.data,
        status=form.status.data,
        roleCode=form.roleCode.data,
        roleDesc=form.roleDesc.data,
    )
    try:
        db.session.add(new_role)
        db.session.commit()
        return resp.succ(data="添加成功")
    except IntegrityError:
        db.session.rollback()
        return resp.succ(data="数据库操作失败")


@systemManage_api.route('/getUserList', methods=['GET'])
def getUserList():
    # 获取 GET 请求中的参数，若没有提供，则使用默认值
    current = request.args.get('current', default=1, type=int)
    size = request.args.get('size', default=10, type=int)
    status = request.args.get('status', default=None, type=int)
    userName = request.args.get('userName', default=None, type=str)
    userGender = request.args.get('userName', default=None, type=int)
    nickName = request.args.get('nickName', default=None, type=str)
    userPhone = request.args.get('userPhone', default=None, type=str)
    userEmail = request.args.get('userEmail', default=None, type=str)

    query = db.session.query(User)


    # 动态添加查询条件
    if status is not None:
        query = query.filter(User.status == status)
    if userName:
        query = query.filter(User.userName.like(f'%{userName}%'))  # 模糊查询
    if userGender is not None:
        query = query.filter(User.userGender == userGender)
    if nickName:
        query = query.filter(User.nickName.like(f'%{nickName}%'))  # 模糊查询
    if userPhone:
        query = query.filter(User.userPhone.like(f'%{userPhone}%'))  # 模糊查询
    if userEmail:
        query = query.filter(User.userEmail.like(f'%{userEmail}%'))  # 模糊查询
    # 获取总数
    total_count = query.count()

    # 执行查询
    ul = query.offset((current - 1) * size).limit(size).all()

    return resp.succ(data={
        "records": [item.to_dict() for item in ul],
        "current": current,
        "size": size,
        "total": total_count
    })


@systemManage_api.route('/userAdd', methods=['POST'])
def userAdd():
    # 判断用户名是否已存在
    existing_user = User.query.filter_by(userName="admin").first()

    if existing_user:
        # 如果用户名已存在，返回错误信息
        return resp.succ(data="用户名已存在")
    else:
        # 用户名不存在，进行新增操作
        new_user = User(
            createBy="admin",
            createTime=datetime.utcnow(),
            userName="john_doe",
            password=generate_password_hash("123456"),
            userGender=1,
            nickName="John",
            userPhone="1234567890",
            userEmail="johndoe@example.com"
        )
        try:
            db.session.add(new_user)
            db.session.commit()
            print("新用户添加成功")
            return resp.succ(data="新用户添加成功")
        except IntegrityError:
            db.session.rollback()
            print("数据库操作失败")
            return resp.succ(data="数据库操作失败")
