import hashlib
from urllib.parse import urlencode

from django import template

register = template.Library()


@register.filter
def gravatar_url(email, size=30):
    default = "identicon"
    email_encoded = email.lower().encode("utf-8")
    email_hash = hashlib.sha256(email_encoded).hexdigest()
    params = urlencode({"d": default, "s": str(size)})
    return f"https://www.gravatar.com/avatar/{email_hash}?{params}"
