import arrow
from marshmallow import Schema, fields, ValidationError, EXCLUDE
from bson import ObjectId
from bson.errors import InvalidId


class BSONObjectId(fields.Field):

    def _serialize(self, value, attr, obj, **kwargs):
        try:
            bson_object_id = ObjectId(value)
        except InvalidId as err:
            raise ValidationError(str(err))
        else:
            return bson_object_id

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            ObjectId(value)
        except InvalidId as err:
            raise ValidationError(str(err))
        else:
            return value


class BaseSchema(Schema):
    _id = BSONObjectId(required=True)
    is_active = fields.Boolean(missing=True)
    created = fields.DateTime(missing=arrow.now())
    last_modified = fields.DateTime(missing=arrow.now())
    order = fields.Integer(missing=0)

    class Meta:
        unknown = EXCLUDE


class CategorySchema(BaseSchema):
    name = fields.String(
        required=True,
        error_messages={'required': {'message': "缺少名称", 'code': 122}}
    )
    type = fields.String(required=True)
    parent = fields.Raw(missing=None)
    total_use = fields.Int(missing=0)
    desc = fields.Str(missing="no desc")


class AccountSchema(BaseSchema):
    name = fields.String(
        required=True,
        error_messages={'required': {'message': "缺少名称", 'code': 122}}
    )
    balance = fields.Int(require=True)  # 余额
    total_income = fields.Int(missing=0)  # 总收入
    total_outlay = fields.Int(missing=0)  # 总支出


class SellerSchema(BaseSchema):
    name = fields.String(
        required=True,
        error_messages={'required': {'message': "缺少名称", 'code': 122}}
    )
    parent = fields.Raw()
    totol_use = fields.Int()
    desc = fields.Str()


class RecordSchema(BaseSchema):
    amount = fields.Int(
        required=True,
        error_messages={'required': {'message': "缺少消费"}}
    )
    type = fields.String(required=True)
    desc = fields.Str()
    date = fields.Date(required=True)
    time = fields.Time(required=True)
    acount = fields.Nested(AccountSchema, only=['_id', 'name'], required=True)
    category = fields.Nested(CategorySchema, only=['_id', 'name'], required=True)
    remark = fields.String()
    totol_use = fields.Int()
