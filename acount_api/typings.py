
from aiohttp.web import Request

from .models import Model, MongoQuery


class RequestType(Request):
    """补充middleware注入的Model"""
    model = Model
