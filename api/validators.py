import re
from django.core.exceptions import ValidationError


class ComplexityPasswordValidator:
    """
    Validates that the password contains at least:
    - 8 characters
    - 1 uppercase letter
    - 1 lowercase letter
    - 1 numeric digit
    """
    def validate(self, password, user=None):
        if len(password) < 8:
            raise ValidationError(
                "The password must be at least 8 characters long.",
                code='password_too_short',
            )
        if not re.search(r'[A-Z]', password):
            raise ValidationError(
                "The password must contain at least one uppercase letter.",
                code='password_no_upper',
            )
        if not re.search(r'[a-z]', password):
            raise ValidationError(
                "The password must contain at least one lowercase letter.",
                code='password_no_lower',
            )
        if not re.search(r'[0-9]', password):
            raise ValidationError(
                "The password must contain at least one numeric digit.",
                code='password_no_number',
            )

    def get_help_text(self):
        return "Your password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one number."
