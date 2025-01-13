from datetime import datetime

from model.connent import db


class User(db.Model):
    __tablename__ = 'users'  # 表名

    # 定义字段与类型
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='用户ID')
    createBy = db.Column(db.String(100), nullable=False, comment='创建人')
    createTime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, comment='创建时间')
    updateBy = db.Column(db.String(100), default=None, comment='更新人')
    updateTime = db.Column(db.DateTime, default=None, onupdate=datetime.utcnow, comment='更新时间')
    status = db.Column(db.SmallInteger, default=True, comment='状态（1 启用，0 禁用）')
    userName = db.Column(db.String(50), nullable=False, comment='用户名')
    password = db.Column(db.String(255), nullable=False, comment='password')
    userGender = db.Column(db.SmallInteger, default=0, comment='性别（0 未知，1 男，2 女）')
    nickName = db.Column(db.String(100), default=None, comment='昵称')
    userPhone = db.Column(db.String(20), default=None, comment='用户电话')
    userEmail = db.Column(db.String(100), default=None, comment='用户邮箱')

    def to_dict(self):
         return {
            "id": self.id,
            "createBy": self.createBy,
            "createTime": self.createTime.isoformat() if self.createTime else None,
            "updateBy": self.updateBy,
            "updateTime": self.updateTime.isoformat() if self.updateTime else None,
            "status": self.status,
            "userName": self.userName,
            # "password": self.password,
            "userGender": self.userGender,
            "nickName": self.nickName,
            "userPhone": self.userPhone,
            "userEmail": self.userEmail
        }
class Role(db.Model):
    __tablename__ = 'roles'  # 表名，与数据库中的表名一致

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='角色ID')
    createBy = db.Column(db.String(100), nullable=False, comment='创建人')
    createTime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, comment='创建时间')
    updateBy = db.Column(db.String(100), default=None, comment='更新人')
    updateTime = db.Column(db.DateTime, default=None, onupdate=datetime.utcnow, comment='更新时间')
    status = db.Column(db.SmallInteger, default=1, comment='状态（1 启用，0 禁用）')
    roleName = db.Column(db.String(100), nullable=False, comment='角色名称')
    roleCode = db.Column(db.String(50), nullable=False, comment='角色编码')
    roleDesc = db.Column(db.Text, comment='角色描述')

    def to_dict(self):
        return {
            "id": self.id,
            "createBy": self.createBy,
            "createTime": self.createTime.isoformat() if self.createTime else None,  # 转换为 ISO 格式的字符串
            "updateBy": self.updateBy,
            "updateTime": self.updateTime.isoformat() if self.updateTime else None,  # 转换为 ISO 格式的字符串
            "status": self.status,
            "roleName": self.roleName,
            "roleCode": self.roleCode,
            "roleDesc": self.roleDesc
        }

class UserRole(db.Model):
    __tablename__ = 'rela_user_role'  # 表名，与数据库中的表名一致

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='ID字段，自动递增')
    userId = db.Column(db.Integer, nullable=False, comment='用户ID')
    roleId = db.Column(db.Integer, nullable=False, comment='角色ID')
    roleCode = db.Column(db.String(50), nullable=False, comment='角色编码')

    def to_dict(self):
        # 使用字典推导式将模型字段转换为字典
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}