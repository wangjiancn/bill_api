import functools
import asyncio

from aiohttp.web import RouteTableDef
import arrow

from ..models import Acount, Category, Record, client
from ..utils import JSONResponse, APIException
from ..typings import RequestType

action_routes = RouteTableDef()
action_func_list = {"get": {}, "post": {}, "delete": {}}
ALLOW_METHODS = ["GET", "POST", "DELETE"]


def register_action(method='get'):
    """注册action

    路由路径格式为: '<HTTPMethod>/action/<FunctionName>'
    """

    def register_action_by_method(func):
        if method.upper() not in ALLOW_METHODS:
            raise ValueError('Method Not Allowed')
        route_func = getattr(action_routes, method.lower())
        route_func(f'/{method.lower()}/action/{func.__name__.lower()}')(func)
        return func
    return register_action_by_method


@register_action()
async def get_cat_tree(r: RequestType):
    """获取分类二级结构

    :return
    :rtype: JSONResonse
    """
    return JSONResponse.success(get_cat_tree.__name__)


@register_action(method='post')
async def create_record(r: RequestType):
    data = await r.json()
    async with await client.start_session() as s:
        async with s.start_transaction():
            tasks = []
            type = data['type']
            amount = data['amount']
            acount = data['acount']
            tasks.append(Category.Query().filter(_id__obj=data['category']['_id']).update(total_use__inc=1))
            if type == 'income':
                tasks.append(Acount.Query().filter(_id__obj=acount['_id']).update(
                    balance__inc=amount, total_income__inc=amount))
            else:
                tasks.append(Acount.Query().filter(_id__obj=acount['_id']).update(
                    balance__inc=-amount, total_outlay__inc=amount))
            tasks.append(Record.create(data))
            await asyncio.gather(*tasks)
        return JSONResponse.success()


@register_action()
async def get_year_report(r: RequestType):
    """获取年度收入支出报表"""
    year = r.query.get('year', '2019')
    res = await Record.Query().collection.aggregate([
        {'$match': {'date': {'$regex': f'^{year}'}}},
        {'$group': {
            '_id': {'type': '$type', 'month': {'$substr': ['$date', 0, 7]}},
            'total': {'$sum': '$amount'}}
         }
    ]).to_list(None)
    month_list = ['{}-{:0>2d}'.format(year, i)for i in range(1, 13)]
    data = []
    month_map = {i: {} for i in month_list}
    for i in res:
        month_map[i['_id']['month']].update({i['_id']['type']: i['total']})
    for month in month_list:
        if month in month_map:
            data.append(dict(name=month, income=month_map[month].get(
                'income', 0), outlay=month_map[month].get('outlay', 0), ))
        else:
            data.append(dict(name=month, income=0, outlay=0))
    return JSONResponse.success(data)
