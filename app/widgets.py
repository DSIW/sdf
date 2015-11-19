from django.forms.widgets import FileInput


class CustomFileInput(FileInput):
    input_type = 'file'

    def render(self, name=None, value=None, attrs=None, single_attrs=None):
        self = ''
        if value is not  None:
            self +='<img width="500px" src="/media/' + value.__str__() + '" />'
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
