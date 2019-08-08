
from pymongo import DESCENDING, ASCENDING

from .schemas import CategorySchema, AccountSchema, RecordSchema, SellerSchema
from .basemodel import Model


class Category(Model):

    Schema = CategorySchema

    class Meta:
        indexes = [
            ([('name', ASCENDING), ('is_active', ASCENDING)], {'unique': True})]


class Acount(Model):

    Schema = AccountSchema

    class Meta:
        indexes = [
            ([('name', ASCENDING), ('is_active', ASCENDING)], {'unique': True})]


class Seller(Model):

    Schema = SellerSchema


class Record(Model):

    Schema = RecordSchema

    class Meta:
        indexes = [
            ([('name', ASCENDING), ('is_active', ASCENDING)], {'unique': True})]
