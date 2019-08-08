from copy import deepcopy
from functools import wraps
import asyncio

from marshmallow import Schema, fields
from motor.core import AgnosticCollection, AgnosticCursor
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING, DESCENDING

from ..settings import MONGO_CONF
from ..utils import codec_options
from .expression import parse_update, parse_filter, and_, or_


def init_mongo(conf, loop=None):
    if not loop:
        loop = asyncio.get_event_loop()
    conn = AsyncIOMotorClient(
        conf['HOST'],
        conf['PORT'],
        maxPoolSize=conf['MAX_POOL_SIZE'],
        io_loop=loop
    )
    db_name = conf['NAME']
    return conn, conn[db_name]


client, db = init_mongo(MONGO_CONF)


class MongoQuery:

    """motor代理

    带下划线的方法表示不能连续链式调用
    """

    db = db

    def __init__(self, collection, Schema):
        self.Schema: Schema = Schema
        self.collection: AgnosticCollection = collection
        self._init_query()

    def _init_query(self):
        self.filter_dict = {}
        self.sort_list = []
        self.skip = 0
        self.limit = 10

    def filter(self, **kwargs):
        self.filter_dict.update(kwargs)
        return self

    @property
    def query_doc(self):
        return parse_filter(self.filter_dict)

    @property
    def cursor(self) -> AgnosticCursor:
        cursor = self.collection.find(parse_filter(self.filter_dict))
        if self.sort_list:
            cursor = cursor.sort(self.sort_list)
        return cursor

    def order_by(self, *args):
        sort_list = []
        for sort_field in args:
            if sort_field.startswith('-'):
                sort_list.append((sort_field[1:-1], DESCENDING))
            else:
                sort_list.append((sort_field, ASCENDING))
        self.sort_list = sort_list
        return self

    def pagination(self, limit=10, offset=0):
        if isinstance(offset, str):
            offset = int(limit)
        if isinstance(limit, str):
            limit = int(limit)
        return self.cursor.skip(offset).limit(limit).to_list(None)

    async def all(self, length=None):
        """返回所有结果"""
        return await self.cursor.to_list(length)

    async def count(self, session=None, **kwargs):
        """返回匹配到的结果数量"""
        return await self.collection.count_documents(self.query_doc, session=None, **kwargs)

    async def update(self, **kwargs):
        """批量更新筛选后的结果"""
        return await self._update_many(self.query_doc, parse_update(kwargs))

    async def update_or_create(self, **kwargs):
        """批量更新筛选后的结果"""
        return await self._update_many(self.query_doc, parse_update(kwargs), upsert=True)

    async def delete(self):
        """批量删除筛选后的结果"""
        return await self._delete_many(self.query_doc)

    async def _create(self, document):
        """插入一条记录"""
        result = await self.collection.insert_one(document)
        return result

    async def _bulk_create(self, documents):
        """批量创建"""
        pass

    async def _update_one(self, cond, data, **kwargs):
        """更新一条记录"""
        return await self.collection.update_one(cond, data, **kwargs)

    async def _update_many(self, cond, data, **kwargs):
        """更新一条记录"""
        return await self.collection.update_many(cond, data, **kwargs)

    async def _delete_one(self, cond):
        """删除一条记录"""
        return await self.collection.delete_one(cond)

    async def _delete_many(self, cond):
        """删除匹配的记录"""
        return await self.collection.delete_many(cond)

    async def _replace_one(self, cond, new_document):
        """替换一条记录"""
        pass


class _QueryMixin:
    @classmethod
    def Query(self):
        return MongoQuery(self.collection, self.Schema)
