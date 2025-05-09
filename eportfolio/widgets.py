from wtforms import StringField
from wtforms.widgets import html_params
from markupsafe import Markup

class ButtonWidget(object):
    input_type = "button"

    html_params = staticmethod(html_params)

    def __call__(self, field, **kwargs):
        kwargs.setdefault("id", field.id)
        kwargs.setdefault("type", self.input_type)

        if "value" not in kwargs:
            kwargs["value"] = field._value()

        label = kwargs.pop('label', field.label.text) if field.label else kwargs.get('value', '')

        return Markup("<button {params}>{label}</button>".format(
            params=self.html_params(name=field.name, **kwargs),
            label=label
        ))

class ButtonField(StringField):
    widget = ButtonWidget()

    def __init__(self, label='', validators=None, **kwargs):
        super().__init__(label, validators, **kwargs)

    def _value(self):
        return self.data if self.data is not None else ''

    def __call__(self, **kwargs):
        return self.widget(self, **kwargs)