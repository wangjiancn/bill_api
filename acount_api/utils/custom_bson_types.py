import datetime

import arrow
from bson.codec_options import TypeRegistry, TypeCodec, CodecOptions
from bson import string_type


class ArrowCodec(TypeCodec):
    python_type = arrow.arrow.Arrow
    bson_type = datetime.datetime

    def transform_python(self, value: arrow.Arrow):
        return value.isoformat()

    def transform_bson(self, value: str):
        return arrow.get(value).datetime


class DateCodec(TypeCodec):
    python_type = datetime.date
    bson_type = string_type

    def transform_python(self, value: datetime.date):
        return value.isoformat()

    def transform_bson(self, value: str):
        return value


class TimeCodec(TypeCodec):
    python_type = datetime.time
    bson_type = string_type

    def transform_python(self, value: datetime.time):
        return value.isoformat()

    def transform_bson(self, value: str):
        return value


type_registry = TypeRegistry([DateCodec(), TimeCodec(), ArrowCodec()])
codec_options = CodecOptions(type_registry=type_registry)
