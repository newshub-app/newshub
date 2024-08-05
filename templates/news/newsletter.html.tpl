<!DOCTYPE html>
<html lang="en">
<body>
<h1>Links curated last week:</h1>
{% for link_group in links %}
    <h4>{{ link_group.category|title }}</h4>
    <ul>
        {% for link in link_group.links %}

            <li>
                <a class="link-dark link-underline-opacity-0 link-underline-opacity-100-hover"
                   href="{{ link.url }}"
                   title="{{ link.url }}"
                   target="_blank"
                >
                    {{ link.title }} <i class="bi bi-box-arrow-up-right"></i>
                </a>
                <small>
                    {% with link.created_by__first_name|add:" "|add:link.created_by__last_name as creator_name %}
                        (shared by {{ creator_name.strip|default:link.created_by__username }})
                    {% endwith %}
                </small>
                <br>
                <p>{{ link.description }}</p>
            </li>
        {% endfor %}
    </ul>
{% endfor %}
<br>
This newsletter can also be read online <a href="#">here</a> along with older editions.
</body>
</html>
