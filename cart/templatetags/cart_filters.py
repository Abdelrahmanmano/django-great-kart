from django import template

register = template.Library()

@register.filter
def sum_field(items, field_name):
    """
    Custom template filter to calculate the sum of a specific field in a queryset or list of dictionaries.
    """
    return sum(getattr(item, field_name, 0) for item in items)

@register.filter
def mul(value, arg):
    """
    Custom template filter to multiply a value by an argument.
    """
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0