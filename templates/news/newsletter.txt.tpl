# Links curated last week:
{% for link_group in links %}
    ## {{ link_group.category|title }}
    {% for link in link_group.links %}
        {% with link.created_by__first_name|add:" "|add:link.created_by__last_name as creator_name %}
            {{ forloop.counter }}. {{ link.title }}: {{ link.url }} (shared by {{ creator_name.strip|default:link.created_by__username }})
        {% endwith %}
        {{ link.description }}
    {% endfor %}
{% endfor %}
This newsletter can also be read online here along with older editions: TODO
