import asyncio

from pymongo import DESCENDING, ASCENDING
from marshmallow import Schema, fields

from .query import _QueryMixin, db
from ..utils import codec_options


RESISTER_MODES = {}


class ModelMetaClass(type):

    class Meta:
        indexes = []

    def __new__(cls, name: str, bases, attrs: dict):
        Meta = attrs.get('Meta')
        if Meta and hasattr(Meta, 'collection_name'):
            collection_name = Meta.collection_name
        else:
            collection_name = name.lower()

        if collection_name != 'model':
            collection = db.get_collection(collection_name, codec_options=codec_options)
            attrs['collection'] = db.get_collection(collection_name, codec_options=codec_options)

            if Meta and hasattr(Meta, 'indexes'):
                if isinstance(Meta.indexes, list) and Meta.indexes:
                    for index in Meta.indexes:
                        collection.create_index(*index)
                else:
                    raise ValueError('Indexes must be list')

        class_ = type.__new__(cls, name, bases, attrs)

        if name != 'Model':
            RESISTER_MODES[name.lower()] = class_
        return class_


class Model(_QueryMixin, metaclass=ModelMetaClass):
    Schema: Schema = None

    class Meta:
        indexes = []

    @classmethod
    async def create(cls, document):
        schema = cls.Schema(partial=("_id",))  # pylint:disable=not-callable
        obj = schema.load(document)
        return await cls.Query()._create(obj)  # pylint:disable=no-member
