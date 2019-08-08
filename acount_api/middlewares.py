from aiohttp.web import middleware,  Request
from aiohttp.web_exceptions import HTTPError
from marshmallow import ValidationError
from bson.errors import InvalidId
from pymongo.errors import DuplicateKeyError

from .models import RESISTER_MODES
from .utils import JSONResponse, APIException


@middleware
async def set_model(request: Request, handler):
    """到RestfulAPI先注入Model对象到request对象

    :param request:(Request) request对象
    :param handler:(func) 视图函数
    :return: response对象
    :rtype: response
    """
    model_name = request.match_info.get('model_name')
    if model_name:
        model = RESISTER_MODES.get(model_name)
        if model:
            request.model = model
        else:
            return JSONResponse.error(1301)
    resp = await handler(request)
    return resp


@middleware
async def validate_error_handler(request, handler):
    try:
        resp = await handler(request)
    # 数据校验错误
    except ValidationError as err:
        return JSONResponse.error(1302, err.messages)
    # ObjectID校验错误
    except InvalidId:
        return JSONResponse.error(1303)
    # 自定已API异常
    except APIException as err:
        return JSONResponse.error(err.code, err.err)
    # 系统HTTP错误
    except HTTPError as err:
        return JSONResponse.error(err.status_code, status=err.status_code)
    # pymongo 唯一索引冲突错误
    except DuplicateKeyError as err:
        return JSONResponse.error(2001, err.details)
    else:
        return resp

middlewares = (set_model, validate_error_handler)
