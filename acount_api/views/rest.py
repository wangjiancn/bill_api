from aiohttp.web import RouteTableDef, Request
from bson import ObjectId

from ..models import Record, RESISTER_MODES
from ..utils import JSONResponse
from ..typings import RequestType

rest_routes = RouteTableDef()
BASE_URL = '/rest'


@rest_routes.get(BASE_URL + '/{model_name}')
async def getRows(request: RequestType):
    order_by = request.query.get('order', '_id')
    limit = request.query.get('limit', 10)
    offset = request.query.get('offset', 0)
    results = await request.model.Query().order_by(order_by).pagination(limit=limit, offset=offset)
    return JSONResponse.success({'objects': results})


@rest_routes.get(BASE_URL + '/{model_name}/{id}')
async def getRow(request: RequestType):
    _id = request.match_info['id']
    row = await request.model.Query().filter(_id=ObjectId(_id)).order_by('total_use').all()
    return JSONResponse.success({'object': row})


@rest_routes.post(BASE_URL + '/{model_name}')
async def createRow(request: RequestType):
    data = await request.json()
    result = await request.model.create(data)
    return JSONResponse.success(result)


@rest_routes.post(BASE_URL + '/{model_name}/{id}')
async def updateRow(request: RequestType):
    data = await request.json()
    _id = request.match_info['id']
    result = request.model.Query().filter(_id=ObjectId(_id)).update(data)
    return JSONResponse.success(result)


@rest_routes.delete(BASE_URL + '/{model_name}/{id}')
async def delete_row(request: RequestType):
    _id = request.match_info['id']
    result = await request.model.Query().filter(_id=ObjectId(_id)).delete()
    return JSONResponse.success(result)
