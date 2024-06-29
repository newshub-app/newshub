from django.test import TestCase
from django.urls import reverse

from .data import *
from ..models import Link


class AuthenticatedRequests(TestCase):
    fixtures = ["categories.json", "admin_user.json"]

    def authenticated_query_test(
        self,
        view_name,
        method="get",
        expected_view=None,
        expected_content=None,
        reverse_kwargs=None,
        **req_kwargs
    ):
        req_method = getattr(self.client, method)
        response = req_method(
            reverse(view_name, kwargs=reverse_kwargs), follow=True, **req_kwargs
        )
        self.assertEqual(response.status_code, 200)
        if expected_view is not None:
            self.assertEqual(response.resolver_match.view_name, expected_view)
        if expected_content:
            self.assertContains(response, expected_content)

    def setUp(self):
        self.client.login(username="admin", password="admin")

    def test_index(self):
        self.authenticated_query_test("news:index", expected_content=INDEX_TITLE)

    def test_link_create(self):
        self.authenticated_query_test(
            "news:link_create",
            method="post",
            expected_content=EXAMPLE_LINK_TITLE,
            data=EXAMPLE_LINK,
        )

    def test_links(self):
        response = self.client.get(reverse("news:links"))
        self.assertContains(response, LINKS_TITLE, status_code=200)

    def test_link_update_get(self):
        self.client.post(reverse("news:link_create"), data=EXAMPLE_LINK)
        response = self.client.get(
            reverse("news:link_update", kwargs={"pk": Link.objects.last().pk})
        )
        self.assertContains(response, LINK_EDIT_TITLE, status_code=200)

    def test_link_update_post(self):
        self.client.post(reverse("news:link_create"), data=EXAMPLE_LINK)
        modified_link = EXAMPLE_LINK.copy()
        modified_link["title"] = UPDATED_TITLE
        response = self.client.post(
            reverse("news:link_update", kwargs={"pk": Link.objects.last().pk}),
            data=modified_link,
            follow=True,
        )
        self.assertContains(response, UPDATED_TITLE, status_code=200)
