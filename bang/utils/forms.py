from django import forms


class DateInputWidget(forms.DateInput):
    input_type = 'date'

    def __init__(self, attrs=None, format='%Y-%m-%d'):
        super().__init__(attrs)
        self.format = format

class DateTimeInputWidget(forms.DateTimeInput):
    input_type = 'datetime-local'

    def __init__(self, attrs=None, format='%Y-%m-%dT%H:%M:%S'):
        super().__init__(attrs)
        self.format = format