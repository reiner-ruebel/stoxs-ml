from flask import Flask, current_app
from flask_restx import Resource, Api
from dependency_injector.wiring import inject, Provide

from app.web.resources import WsgiServices

print('importing controller test')

@inject
def get_app(app: Flask = Provide[WsgiServices.app]) -> Flask:
    return app

WsgiServices().wire(modules=[__name__])

app = current_app
# api = Api(app, title="my title")
# print('api title', api.title)

@app.route('/hello')
def hello():
    return {'hello': 'world'}

# @api.route('/hello')
# class HelloWorld(Resource):
#     print('init class')
#     def get(self):
#         return {'hello': 'world'}


# # from app.services.test.itest_service import ITestService
# # from app.services.test.test_service import TestService


# @inject
# def get_api(api: Api = Provide[WsgiServices.api]) -> Api:
#     return api

# WsgiServices().wire(modules=[__name__])

# api = get_api()
# #test_service: ITestService = TestService()

# @api.route('/test')
# class TestController(Resource):
#     def get(self) -> dict[str, str]:
#         return {"hello": "my dear friend"}
# #        return test_service.hello()

