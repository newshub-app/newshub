{% load userlinks %}
# Links curated last week:
{% regroup newsletter.get_links_data by category__name as links_by_cat %}
{% for links in links_by_cat %}
    {% user_has_category_subscription user links.grouper as has_cat %}
    {% if has_cat %}
        ## {{ links.grouper|title }}
        {% for link in links.list %}
            {% with link.created_by__first_name|add:" "|add:link.created_by__last_name as creator_name %}
                {{ forloop.counter }}. {{ link.title }}: {{ link.url }} (shared by {{ creator_name.strip|default:link.created_by__username }})
            {% endwith %}
            {{ link.description }}
        {% endfor %}
    {% endif %}
{% endfor %}
This newsletter can also be read online here along with older editions: TODO
