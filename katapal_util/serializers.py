from __future__ import unicode_literals, absolute_import

from django.utils.translation import ugettext_lazy as _l
from phonenumber_field.phonenumber import to_python
from phonenumber_field.validators import validate_international_phonenumber
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, CharField


class HasProviderSerializer(ModelSerializer):

    def load_provider(self, data):
        try:
            if "id" in data:
                return self.Meta.model.objects.get(pk=data["id"])
            else:
                kwargs = {}
                if "name" in data:
                    kwargs["name"] = data["name"]
                if "account" in data:
                    kwargs["account"] = data["account"]
                return self.Meta.model.objects.get(**kwargs)
        except self.Meta.model.DoesNotExist:
            raise ValidationError("Unable to retrieve provider")


class PhoneNumberField(CharField):
    """
    Assume the number starts with a country code.  To convert to internal
    representation, simply prepend "+".  To convert to external, remove the
    leading "+"
    """

    default_error_messages = {
        'invalid': _l('Enter a valid phone number.'),
    }

    default_validators = [validate_international_phonenumber]

    def to_internal_value(self, data):
        return "+" + data

    def to_representation(self, value):
        phonenumber = to_python(value)
        if phonenumber.is_valid():
            return str(phonenumber)[1:] # remove leading +
