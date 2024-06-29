from django.test import TestCase
from django.urls import reverse

from authnz.models import User
from .data import *
from ..models import *


class AuthenticationEnforced(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create_user(
            username=USER1_USERNAME, password=USER_PASSWORD
        )
        cls.test_category = Category.objects.create(name="SampleCategory")
        link_data = EXAMPLE_LINK.copy()
        link_data["category"] = cls.test_category
        link_data["created_by"] = cls.test_user
        cls.test_link = Link.objects.create(**link_data)

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
        self.unauthenticated_query_test(
            "news:link_update", reverse_kwargs={"pk": Link.objects.last().pk}
        )

    def test_link_update_post(self):
        modified_link = EXAMPLE_LINK.copy()
        modified_link["title"] = UPDATED_TITLE
        self.unauthenticated_query_test(
            "news:link_update",
            method="post",
            reverse_kwargs={"pk": Link.objects.last().pk},
            data=modified_link,
        )
