from django.core.exceptions import ValidationError
from django.core.validators import validate_email


def is_email_valid(value):
    # Validate a single email
    message_invalid = "Enter a valid email address"

    if not value:
        return False, message_invalid

    # Check the regex, using the validate_email from django
    try:
        validate_email(value)
    except ValidationError:
        return False, message_invalid

    return True, ""
