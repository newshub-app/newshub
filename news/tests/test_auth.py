from django.test import TestCase
from django.urls import reverse

from .data import *


class AuthenticationEnforced(TestCase):
    def unauthenticated_query_test(
        self, view_name, method="get", reverse_kwargs=None, **req_kwargs
    ):
        req_method = getattr(self.client, method)
        response = req_method(
            reverse(view_name, kwargs=reverse_kwargs), follow=True, **req_kwargs
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.view_name, "authnz:login")

    def test_index(self):
        self.unauthenticated_query_test("news:index")

    def test_link_create(self):
        self.unauthenticated_query_test("news:link_create")

    def test_links(self):
        self.unauthenticated_query_test("news:links")

    def test_link_update_get(self):
        self.unauthenticated_query_test("news:link_update", reverse_kwargs={"pk": 1})

    def test_link_update_post(self):
        modified_link = EXAMPLE_LINK.copy()
        modified_link["title"] = UPDATED_TITLE
        self.unauthenticated_query_test(
            "news:link_update",
            method="post",
            reverse_kwargs={"pk": 1},
            data=modified_link,
        )
