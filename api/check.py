from flask import Blueprint

# 创建一个 Blueprint，命名为 user
check_api = Blueprint('check', __name__)

# 定义 GET 请求接口
@check_api.get("get")
def login_get():
    return {"a":"get"}

# 定义 POST 请求接口
@check_api.route('/post', methods=['POST'])
def login_post():
    return {"a":"post"}


