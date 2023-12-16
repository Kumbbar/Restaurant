import django.contrib.auth.password_validation as validators


def validate_password(password: str) -> str:
    validators.validate_password(password=password)
    return password