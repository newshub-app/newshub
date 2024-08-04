from django import template

register = template.Library()


@register.simple_tag
def user_has_category_subscription(user, category):
    return user.subscribed_categories.filter(name=category).exists()
