from django.forms.widgets import FileInput


class MultipleFileInput(FileInput):
    def __init__(self, attrs=None):
        default_attrs = {'multiple': 'multiple'}
        if attrs:
            default_attrs.update(attrs)
        super(MultipleFileInput, self).__init__(default_attrs)

    def value_from_datadict(self, data, files, name):
        if not files:
            return None
        return files.getlist(name)
