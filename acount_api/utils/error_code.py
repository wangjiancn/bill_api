""" 错误码
code < 0 系统级别错误
code = 0 返回正常
code > 0 业务错误
"""

_http_status_code = {
    100: {
        'en': 'Continue',
        'zh': '继续。客户端应继续其请求'},
    101: {
        'en': 'Switching Protocols',
        'zh': '切换协议。服务器根据客户端的请求切换协议。只能切换到更高级的协议，例如，切换到HTTP的新版本协议'},
    200: {
        'en': 'OK',
        'zh': '请求成功。一般用于GET与POST请求'},
    201: {
        'en': 'Created',
        'zh': '已创建。成功请求并创建了新的资源'},
    202: {
        'en': 'Accepted',
        'zh': '已接受。已经接受请求，但未处理完成'},
    203: {
        'en': 'Non-Authoritative Information',
        'zh': '非授权信息。请求成功。但返回的meta信息不在原始的服务器，而是一个副本'},
    204: {
        'en': 'No Content',
        'zh': '无内容。服务器成功处理，但未返回内容。在未更新网页的情况下，可确保浏览器继续显示当前文档'},
    205: {
        'en': 'Reset Content',
        'zh': '重置内容。服务器处理成功，用户终端（例如：浏览器）应重置文档视图。可通过此返回码清除浏览器的表单域'},
    206: {
        'en': 'Partial Content',
        'zh': '部分内容。服务器成功处理了部分GET请求'},
    300: {
        'en': 'Multiple Choices',
        'zh': '多种选择。请求的资源可包括多个位置，相应可返回一个资源特征与地址的列表用于用户终端（例如：浏览器）选择'},
    301: {
        'en': 'Moved Permanently',
        'zh': '永久移动。请求的资源已被永久的移动到新URI，返回信息会包括新的URI，浏览器会自动定向到新URI。今后任何新的请求都应使用新的URI代替'},
    302: {
        'en': 'Found',
        'zh': '临时移动。与301类似。但资源只是临时被移动。客户端应继续使用原有URI'},
    303: {
        'en': 'See Other',
        'zh': '查看其它地址。与301类似。使用GET和POST请求查看'},
    304: {
        'en': 'Not Modified',
        'zh': '未修改。所请求的资源未修改，服务器返回此状态码时，不会返回任何资源。客户端通常会缓存访问过的资源，通过提供一个头信息指出客户端希望只返回在指定日期之后修改的资源'},
    305: {
        'en': 'Use Proxy',
        'zh': '使用代理。所请求的资源必须通过代理访问'},
    306: {
        'en': 'Unused',
        'zh': '已经被废弃的HTTP状态码'},
    307: {
        'en': 'Temporary Redirect',
        'zh': '临时重定向。与302类似。使用GET请求重定向'},
    400: {
        'en': 'Bad Request',
        'zh': '客户端请求的语法错误，服务器无法理解'},
    401: {
        'en': 'Unauthorized',
        'zh': '请求要求用户的身份认证'},
    402: {
        'en': 'Payment Required',
        'zh': '保留，将来使用'},
    403: {
        'en': 'Forbidden',
        'zh': '服务器理解请求客户端的请求，但是拒绝执行此请求'},
    404: {
        'en': 'Not Found',
        'zh': '服务器无法根据客户端的请求找到资源（网页）。通过此代码，网站设计人员可设置"您所请求的资源无法找到"的个性页面'},
    405: {
        'en': 'Method Not Allowed',
        'zh': '客户端请求中的方法被禁止'},
    406: {
        'en': 'Not Acceptable',
        'zh': '服务器无法根据客户端请求的内容特性完成请求'},
    407: {
        'en': 'Proxy Authentication Required',
        'zh': '请求要求代理的身份认证，与401类似，但请求者应当使用代理进行授权'},
    408: {
        'en': 'Request Time-out',
        'zh': '服务器等待客户端发送的请求时间过长，超时'},
    409: {
        'en': 'Conflict',
        'zh': '服务器完成客户端的 PUT 请求时可能返回此代码，服务器处理请求时发生了冲突'},
    410: {
        'en': 'Gone',
        'zh': '客户端请求的资源已经不存在。410不同于404，如果资源以前有现在被永久删除了可使用410代码，网站设计人员可通过301代码指定资源的新位置'},
    411: {
        'en': 'Length Required',
        'zh': '服务器无法处理客户端发送的不带Content-Length的请求信息'},
    412: {
        'en': 'Precondition Failed',
        'zh': '客户端请求信息的先决条件错误'},
    413: {
        'en': 'Request Entity Too Large',
        'zh': '由于请求的实体过大，服务器无法处理，因此拒绝请求。为防止客户端的连续请求，服务器可能会关闭连接。如果只是服务器暂时无法处理，则会包含一个Retry-After的响应信息'},
    414: {
        'en': 'Request-URI Too Large',
        'zh': '请求的URI过长（URI通常为网址），服务器无法处理'},
    415: {
        'en': 'Unsupported Media Type',
        'zh': '服务器无法处理请求附带的媒体格式'},
    416: {
        'en': 'Requested range not satisfiable',
        'zh': '客户端请求的范围无效'},
    417: {
        'en': 'Expectation Failed',
        'zh': '服务器无法满足Expect的请求头信息'},
    500: {
        'en': 'Internal Server Error',
        'zh': '服务器内部错误，无法完成请求'},
    501: {
        'en': 'Not Implemented',
        'zh': '服务器不支持请求的功能，无法完成请求'},
    502: {
        'en': 'Bad Gateway',
        'zh': '作为网关或者代理工作的服务器尝试执行请求时，从远程服务器接收到了一个无效的响应'},
    503: {
        'en': 'Service Unavailable',
        'zh': '由于超载或系统维护，服务器暂时的无法处理客户端的请求。延时的长度可包含在服务器的Retry-After头信息中'},
    504: {
        'en': 'Gateway Time-out',
        'zh': '充当网关或代理的服务器，未及时从远端服务器获取请求'},
    505: {
        'en': 'HTTP Version not supported',
        'zh': '服务器不支持请求的HTTP协议的版本，无法完成处理'}}

_error_code = {
    -1: dict(
        en='Unkown Error',
        zh="未知错误"
    ),
    # success
    0: dict(
        en='OK',
        zh="成功"
    ),

    # system level code
    1001: dict(
        en="require login",
        zh='需要登录'),
    1003: dict(
        en="missing argument",
        zh='参数错误'),
    1004: dict(
        en="articel not exist",
        zh='资源不存在'),
    1005: dict(
        en="user authenticate failed",
        zh='用户名或密码错误'),
    1006: dict(
        en="Invlid token",
        zh='无效的Token'),
    1007: dict(
        en="expire token",
        zh='过期的Token'),
    1008: dict(
        en="Illegal model name",
        zh='非法的Model名称'),
    1009: dict(
        en="Illegal operation",
        zh="非法操作"
    ),
    1101: dict(
        en="action not exist",
        zh="该操作不存在"
    ),
    1201: dict(
        en="ext not allow",
        zh="不支持的文件类型"
    ),
    1202: dict(
        en="file not exists",
        zh="未找到文件"
    ),
    1301: dict(
        en="model not exists",
        zh="未找到Model"
    ),
    1302: dict(
        en="field not allowed",
        zh="非法字段"
    ),
    1303: dict(
        en="invalid ObjectId",
        zh="非法ObjectId"
    ),
    1010: dict(
        en="action_not_found",
        zh="未找到动作"
    ),
    2001: dict(
        en="duplicate key",
        zh="重复的值"
    )

    # server level code
}

BLANK_MSG = dict(en="No Msg", zh="无错误详细信息")

_code = {**_http_status_code, **_error_code}


def get_msg(code=0, lang=''):
    """根据错误码返回对象中/英文提示 

    :param lang(str): zh/en
    :param code(int): 错误码
    """
    msgs = _code.get(code) or BLANK_MSG
    msg = msgs.get(lang) or msgs.get('en')
    return msg
