# -*- coding: utf-8 -*-
import tornado.gen
import tornado.concurrent
from app.admin.views_admin import AdminHandler
class IndexHandler(AdminHandler):
    @tornado.gen.coroutine
    def get(self,*args,**kwargs):
        #self.write("<h1 style='color:#8b8b8b'>这是后台管理系统！</h1>")
        yield self.get_response()
    @tornado.concurrent.run_on_executor
    def get_response(self):
        self.html('admin/index.html')