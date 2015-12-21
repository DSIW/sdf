# -*- coding: utf-8 -*-

from django.forms.widgets import FileInput

from sdf import settings


class CustomFileInput(FileInput):
    input_type = 'file'

    def render(self, name=None, value=None, attrs=None, single_attrs=None):
        self = ''
        if value:
            self +='<img src="/media/' + str(value) + '" />'
        else:
            value = ''
        self += '''
            <div class="file-field input-field">
              <div class="btn">
                <span>File</span>
                <input type="file" id="''' + name + '''" name="''' + name + '''" >
              </div>
              <div class="file-path-wrapper">
                <input class="file-path validate" value="''' + str(value) + '''" type="text">
              </div>
            </div>
          <label class="active" for="''' + name + '''"><br />Bild (max. ''' + str(settings.FILESIZE_LIMIT_MB) + ''' MB)</label>
'''
        return self
