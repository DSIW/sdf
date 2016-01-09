# -*- coding: utf-8 -*-

from file_resubmit.admin import AdminResubmitImageWidget


from sdf import settings


class CustomFileInput(AdminResubmitImageWidget):
    input_type = 'file'

    def render(self, name=None, value=None, attrs=None, single_attrs=None):
        output = ''
        output += '''
            <div class="file-field input-field">
              <div class="btn">
                <span>Datei</span>
                <input type="file" id="''' + name + '''" name="''' + name + '''" >
              </div>
              <div class="file-path-wrapper">'''
        output += self.output_extra_data(value)
        output += '''</div>
            </div>
          <label class="active" for="''' + name + '''"><br />Bild (max. ''' + str(settings.FILESIZE_LIMIT_MB) + ''' MB)</label>
        '''

        return output
