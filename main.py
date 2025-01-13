from flask import Flask,request
from model.connent import db_init

# 创建 Flask 应用实例
app = Flask(__name__)

# 配置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:HbmimaIs...ijn@172.16.9.103:6001/nova_admin'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'flask_wtf_secret_key'  # Flask-WTF 需要一个 secret_key
app.config['WTF_CSRF_ENABLED'] = False  # 启用 CSRF 保护
app.config['SQLALCHEMY_ECHO'] = True    # 配置 SQLAlchemy 日志，显示 SQL 查询
db_init(app)

from api.check import check_api
from api.auth import auth_api
from api.systemManage import systemManage_api
# 注册 api
app.register_blueprint(check_api, url_prefix='/check')
app.register_blueprint(auth_api, url_prefix='/auth')
app.register_blueprint(systemManage_api, url_prefix='/systemManage')

from api.middleware import check_authorization

# 在每个请求之前校验 Authorization 参数
@app.before_request
def before_request():
    # 排除 auth.login 路由的请求，不进行校验
    if request.endpoint in ['auth.login']:
        return None  # 不进行校验，继续处理请求
    # 否则进行 Authorization 校验
    response = check_authorization()
    if response:
        return response  # 如果验证失败，直接返回错误响应

if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=9980
    )