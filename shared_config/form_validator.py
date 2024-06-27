import datetime

from rest_framework import serializers


class NumericFieldValidator:
    """
    class used for numeric field validation
    """
    def __call__(self, data):
        if not data.isdigit():
            msg = "This field should have numeric value only"
            raise serializers.ValidationError(msg)


class LengthFieldValidator:
    """
    class used for validation of length of string
    """
    def __init__(self, length):
        self.length = length

    def __call__(self, data):
        if len(data) > self.length:
            msg = "This field should have maximum %d characters" % self.length
            raise serializers.ValidationError(msg)


class MinLengthFieldValidator:
    """
    class used for validation of min length of string
    """
    def __init__(self, length):
        self.length = length

    def __call__(self, data):
        if len(data) < self.length:
            msg = "This field should have minimum %d characters" % self.length
            raise serializers.ValidationError(msg)


class CharFieldValidator:
    """
    class validator fo validating string should have char or spaces
    """
    def __init__(self, allowed_special_char=''):
        self.allowed_special_char = allowed_special_char

    def __call__(self, data):
        if not all(ch.isalpha() or ch.isspace() or ch in self.allowed_special_char for ch in data):
            msg = "This field should have only character or spaces"
            raise serializers.ValidationError(msg)


class CharNumericFieldValidator:
    """
    class validator for validating string should have char, spaces or numbers
    """
    def __init__(self, allowed_special_char=''):
        self.allowed_special_char = allowed_special_char

    def __call__(self, data):
        if not all(ch.isalpha() or ch.isspace() or ch.isdigit() or ch in self.allowed_special_char for ch in data):
            msg = "This field should have only character, spaces or numbers "
            raise serializers.ValidationError(msg)


class DateFormatValidator:
    """
    class validator for checking date format is correct or not
    """
    def __init__(self, date_format):
        self.date_format = date_format

    def __call__(self, data):
        try:
            datetime.datetime.strptime(data, self.date_format)
        except:
            msg = "Incorrect date format, should be %s" % self.date_format
            raise serializers.ValidationError(msg)
