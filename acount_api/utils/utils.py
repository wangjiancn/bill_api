import datetime
import json
from collections import namedtuple
from functools import partial
from typing import NamedTuple

import arrow
from aiohttp.web import json_response as _json_response
from aiohttp.web_exceptions import HTTPException
from bson import ObjectId
from pymongo.results import _WriteResult as Result

from .error_code import get_msg


class MyJSONEncoder(json.JSONEncoder):
    """增加对ObjectId序列化的支持"""

    def default(self, obj):  # pylint: disable=E0202
        if isinstance(obj, (datetime.datetime)):
            return arrow.get(obj).isoformat()
        if isinstance(obj, ObjectId):
            return str(obj)
        # 序列化写入结果
        if isinstance(obj, Result):
            dirs = dir(obj)
            can_read_dirs = [
                attr for attr in dirs if not attr.startswith('_')]
            return {key: getattr(obj, key) for key in can_read_dirs}
        return super().default(obj)


dumps = partial(json.dumps, cls=MyJSONEncoder)
json_response = partial(_json_response, dumps=dumps)


def json_response_success(data: dict = None):
    """返回请求成功JSON

    :param data: 返回的对象, defaults to None
    :type data: dict, optional
    :return: JSON,格式:{
        "code": 0,
        "msg": 'OK',
        "data": data
    }
    """
    return json_response({
        "code": 0,
        "msg": get_msg(code=0, lang='en'),
        "data": data
    })


def json_response_error(code=-1, err: str = None, status=200):
    """返回错误信息

    :param code:(int) 错误码, defaults to -1
    :param err:(str optional) 错误信息, defaults to None
    :param status:(int) HTTP状态码
    :return: JSON,格式:{
        "code": 2,
        "msg": 'err message',
        "detail": 'extra err message'
    }
    """

    return json_response({
        "code": code,
        "msg": get_msg(code=code, lang='en'),
        "detail": err
    }, status=status)


class JSONResponse(NamedTuple):
    success = json_response_success
    error = json_response_error


class APIException(HTTPException):
    def __init__(self, code=-1, err: str = None):
        self.code = code
        self.err = err
