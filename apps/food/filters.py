from django.template.defaulttags import register


@register.filter
def format_date(value) -> str:
    return value.strftime('%Y.%m.%d %H:%M')