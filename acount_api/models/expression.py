import re
from bson import ObjectId


QUERY_OPERATOR_MAP = {    # 查询 投影 操作符
    # 比较
    "eq": {"value": "$eq", "fn": lambda x: x},
    "gt": {"value": "$gt", "fn": lambda x: x},
    "gte": {"value": "$gte", "fn": lambda x: x},
    "in": {"value": "$in", "fn": lambda x: x},
    "lt": {"value": "$lt", "fn": lambda x: x},
    "lte": {"value": "$lte", "fn": lambda x: x},
    "ne": {"value": "$ne", "fn": lambda x: x},
    "nin": {"value": "$nin", "fn": lambda x: x},
    "raw": {"value": "", "fn": lambda x: x},
    "startswith": {"value": "$regex", "fn": lambda x: f"^{x}"},
    "contains": {"value": "$regex", "fn": lambda x: f".*{x}"},
    "icontains": {"value": "$regex", "fn": lambda x: f".*{x}/i"},
    # 类型转化
    "obj": {"value": "$eq", "fn": lambda x: ObjectId(x)},
}

UPDATE_OPERATOR_MAP = {
    "inc": {"value": "$inc", "fn": lambda x: x},
    "current": {"value": "$currentDate", "fn": lambda x: x},
    "rename": {"value": "$rename", "fn": lambda x: x},
    "unset": {"value": "$unset", "fn": lambda: ''},
}

"""
逻辑运算符:

同时满足所有条件
{ $and: [ { <expression1> }, { <expression2> } , ... , { <expressionN> } ] }

不同时满足所有条件
{ $nor: [ { <expression1> }, { <expression2> }, ...  { <expressionN> } ] } 

满足任一条件:
{ $or: [ { <expression1> }, { <expression2> }, ... , { <expressionN> } ] }

不满足某一条件
{ field: { $not: { <operator-expression> } } }

"""


def parse_query_field(field: str, value) -> dict:
    field_arr = field.rsplit('__')
    length = len(field_arr)
    field_name = field_arr[0]
    lookup = ''
    if length > 1:
        lookup = field_arr[1]
    if lookup:
        operator = QUERY_OPERATOR_MAP.get(lookup)
        if not operator:
            return None
        if operator['value'] == '':
            return (field_name, operator['fn'](value))
        return (field_name, {operator['value']: operator['fn'](value)})
    else:
        return (field_name, {'$eq': value})


def parse_filter(query: dict) -> dict:
    """返回一个查询文档

    :param filter_document:(dict) filed__lookup
    :return: 查询文档
    :rtype: dict

    >>> parse_filter(dict(num__gt=1))
    {'num': {'$gt': 1}}

    >>> parse_filter(dict(num=1))
    {'num': {'$eq': 1}}

    >>> parse_filter(dict(num=60,num__gt=100,num__lte=20,age__gte=18,age__lte=70))
    {'num': {'$eq': 60, '$gt': 100, '$lte': 20}, 'age': {'$gte': 18, '$lte': 70}}

    >>> parse_filter(dict(datetime__startswith='2018-08',name__icontains="hello"))
    {'datetime': {'$regex': '/^2018-08/'}, 'name': {'$regex': '/.*hello/i'}}
    """

    filter_document = {}
    for field, value in query.items():
        parse_result = parse_query_field(field, value)
        if parse_result:
            field_name = parse_result[0]
            field_value = parse_result[1]
            field_document = filter_document.get(field_name)  # 已有字段的查询值
            if not field_name in filter_document:
                filter_document[field_name] = field_value
            elif isinstance(field_document, (str, int, float)):
                filter_document[field_name] = {'$eq': field_document}
                filter_document[field_name].update(field_value)
            elif isinstance(field_value, (str, int, float)):
                filter_document[field_name].update({'$eq': field_value})
            else:
                filter_document[field_name].update(field_value)

    return filter_document


def or_(filter_document: dict) -> dict:
    return {'$or': parse_filter(filter_document)}


def nor_(filter_document: dict) -> dict:
    return {'$nor': parse_filter(filter_document)}


def and_(filter_document: dict) -> dict:
    return {'$and': parse_filter(filter_document)}


def parse_update_field(field: str, value) -> dict:
    field_arr = field.rsplit('__')
    length = len(field_arr)
    field_name = field_arr[0]
    lookup = ''
    if length > 1:
        lookup = field_arr[1]
    if lookup:
        operator = UPDATE_OPERATOR_MAP.get(lookup)
        if not operator:
            return
        return (operator['value'], {field_name: operator['fn'](value)})
    else:
        return ('$set', {field_name: value})


def parse_update(query: dict) -> dict:
    """返回一个更新操作文档

    :param filter_document:(dict) filed__lookup
    :return: 更新操作文档
    :rtype: dict

    >>> parse_update(dict(num__inc=1))
    {'$inc': {'num': 1}}

    >>> parse_update(dict(num=1,created__current='',score__inc=-1,sorted__inc=10))
    {'$set': {'num': 1}, '$currentDate': {'created': ''}, '$inc': {'score': -1, 'sorted': 10}}

    """

    update_document = {}
    for field, value in query.items():
        parse_result = parse_update_field(field, value)
        if parse_result:
            field_name = parse_result[0]
            field_value = parse_result[1]
            if not field_name in update_document:
                update_document[field_name] = field_value
            else:
                update_document[field_name].update(field_value)
    return update_document


if __name__ == "__main__":
    import doctest
    doctest.testmod()
