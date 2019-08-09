# bill_api
记账应用后端API接口

## API

- [rest.py](./acount_api/views/rest.py):Restful API 
- [action.py](./acount_api/views/action.py):注册动作,对复杂业务逻辑处理
- [models.py](./acount_api/models/models.py):封装一层Model,简化Mongo查询操作
- [middlewares](./acount_api/middlewares.py):中间件,处理错误信息,注入model
- [utils](./acount_api/utils):通用,自定义JSON解析器,BSON解析器,统一返回格式等
