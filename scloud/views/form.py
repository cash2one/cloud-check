# -*- coding: utf-8 -*-

import os
import scloud
from scloud.handlers import Handler
from scloud.shortcuts import url


@url("/form", name="form")
class FormHandler(Handler):
    def get(self):
        return self.render("form.html")

    def post(self):
        upload_path=os.path.join(scloud.base_path, 'static','files')  #文件的暂存路径
        file_metas=self.request.files['file']    #提取表单中‘name’为‘file’的文件元数据
        for meta in file_metas:
            filename=meta['filename']
            filepath=os.path.join(upload_path,filename)
            with open(filepath,'wb') as up:      #有些文件需要已二进制的形式存储，实际中可以更改
                up.write(meta['body'])
            self.redirect(self.reverse_url("form"))
