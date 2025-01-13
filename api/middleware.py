import datetime

import jwt
from flask import request, jsonify,g

jtw_secret_key = "xxxx"
jtw_refresh_secret_key = "refresh_xxxx"


# 自定义校验 Authorization 头的函数
def check_authorization():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        # 如果没有 Authorization 头，返回 401 未授权错误
        return jsonify({"message": "Authorization header is missing"}), 401

    # 检查 Authorization 头的格式是否为 "Bearer <token>"
    if not auth_header.startswith('Bearer '):
        return jsonify({"message": "Authorization format is invalid"}), 401

    # 获取 token
    token = auth_header[len('Bearer '):]
    # 这里可以进一步检查 token 是否有效，比如解码 JWT 或其他操作
    payload = verify_token(token)
    if payload is None:  # 假设 'valid_token' 是有效的 token
        return jsonify({"message": "Invalid token"}), 401
    g.uid=payload['uid']
    # 如果验证通过，返回 None，表示不需要额外处理
    return None


# 生成 JWT token
def generate_token(uid):
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # 设置 1 小时有效期
    token = jwt.encode({
        'uid': uid,
        'exp': expiration_time
    }, jtw_secret_key, algorithm='HS256')
    return token


# 生成 Refresh JWT Token
def generate_refresh_token(uid):
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(days=7)  # 7天有效期
    token = jwt.encode({
        'uid': uid,
        'exp': expiration_time
    }, jtw_refresh_secret_key, algorithm='HS256')
    return token


# 验证 JWT token
def verify_token(token):
    try:
        # 解码 token，如果过期会抛出异常
        payload = jwt.decode(token, jtw_secret_key, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token 过期
    except jwt.InvalidTokenError:
        return None  # 无效的 token


# 验证 JWT refresh token
def verify_refresh_token(token):
    try:
        # 解码 token，如果过期会抛出异常
        payload = jwt.decode(token, jtw_refresh_secret_key, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token 过期
    except jwt.InvalidTokenError:
        return None  # 无效的 token
