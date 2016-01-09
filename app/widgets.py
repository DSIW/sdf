# -*- coding: utf-8 -*-

from file_resubmit.admin import AdminResubmitImageWidget
import re

from sdf import settings


class CustomFileInput(AdminResubmitImageWidget):
    input_type = 'file'

    def render(self, name=None, value=None, attrs=None, single_attrs=None):
        output = ''

        if value is not None and re.match("^images\/(books\/book_|user\/user_)\d+\.", str(value)) is not None:
            output +='<img src="/media/' + str(value) + '" />'
        else:
            output = ''
        output += '''
            <div class="file-field input-field">
              <div class="btn">
                <span>Datei</span>
                <input type="file" id="''' + name + '''" name="''' + name + '''" >
              </div>
              <div class="file-path-wrapper">'''
        if self.output_extra_data(value):
            output += self.output_extra_data(value)
        else:
            output += '''<input class="file-path validate" value="''' + str(value) + '''" type="text">'''
        output += '''</div>
            </div>
          <label class="active" for="''' + name + '''"><br />Bild (max. ''' + str(settings.FILESIZE_LIMIT_MB) + ''' MB)</label>
        '''

        return output
