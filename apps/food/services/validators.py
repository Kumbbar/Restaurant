from django.core.exceptions import ValidationError


def validate_phone_number(phone_number: str):
    if '+' not in phone_number:
        raise ValidationError(
            'phone number must contain +',
        )
    if not phone_number[1:].isdigit():
        raise ValidationError(
            'phone number must be in format +number. Without ()space- symbols',
        )

