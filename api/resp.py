def succ(code=200, data=None):
    """
    返回成功的响应，代码为 200
    :param data: 需要返回的数据，默认为 None
    :return: Response 对象
    """
    return {
        "code": code,
        "msg": "SUCCESS",
        "data": data
    }


def err(code=400, msg="Error"):
    """
    返回错误的响应，代码可以自定义，默认为 400
    :param code: 错误代码，默认为 400
    :param msg: 错误消息，默认为 "Error"
    :param data: 错误相关的数据，默认为 None
    :return: Response 对象
    """
    return {
        "code": code,
        "msg": msg,
        "data": None
    }
