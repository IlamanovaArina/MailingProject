from django import template

register = template.Library()


@register.filter()
def media_filter(user):
    if user:
        return f"/media/{user}"
    return "#"
