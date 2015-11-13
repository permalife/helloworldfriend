from django import forms

from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DateTimeFromStringField(forms.Field):
    """
    Create a custom form field for converting datetime strings
    to valid greeting times represented by native python datetime objects
    """
    def to_python(self, value):
        """
        Convert a string to a valid greeting time
        """
        try:
            if len(value) != 14:
                raise
            dt = datetime.strptime(value, '%Y%m%d%H%M%S')
        except Exception as e:
            # invalid date format
            logger_msg = " ".join([
                "Invalid date format (expected date of the",
                "form YYYYMMDDHHMMSS)",
            ])
            logger.error("%s: %s (%s)", logger_msg, e.message, type(e))
            raise forms.ValidationError(logger_msg, code='invalid')

        utcnow = datetime.utcnow()
        if utcnow > dt:
            logger_msg = " ".join([
                "Requested greeting time is in the past.",
                "Please try again with a future greeting time.",
            ])
            logger.error(logger_msg)
            raise forms.ValidationError(logger_msg, code='invalid')

        return dt

    def validate(self, value):
        """
        Make sure the field is always a native python datetime
        """
        super(DateTimeFromStringField, self).validate(value)
        if not isinstance(value, datetime):
            raise forms.ValidationError(
                "Invalid date string: %(value)s",
                code='invalid',
                params={'value': value}
            )


class GreetingForm(forms.Form):
    """
    Django form to be populated using data provided in the request
    """
    name = forms.CharField()
    datetime = DateTimeFromStringField()
