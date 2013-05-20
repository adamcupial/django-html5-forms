from django.core.validators import RegexValidator


class TelephoneValidator(RegexValidator):
    """Loose validator for telephone numbers.
    This doesn't guarantee a given number is valid, but failing numbers are
    invalid.
    """
    def __init__(self, message=None):
        regex = r'\+?[0-9\-\(\)]+'
        super(TelephoneValidator, self).__init__(regex, message)
