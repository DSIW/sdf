# -*- coding: utf-8 -*-

from django.forms.widgets import FileInput


class CustomFileInput(FileInput):
    input_type = 'file'

    def render(self, name=None, value=None, attrs=None, single_attrs=None):
        self = ''
        if value is not None and bool(value) is not False:
            self +='<a href="' + value.url + '"><img width="500px" src="' + value.url + '" /></a>'
        self += '''
            <div class="file-field input-field">
              <div class="btn">
                <span>File</span>
                <input type="file" name="''' + name + '''" >
              </div>
              <div class="file-path-wrapper">
                <input class="file-path validate" value="''' + value.__str__() + '''" type="text">
              </div>
            </div>'''
        return self
