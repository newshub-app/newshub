from django.test import TestCase

EXAMPLE_LINK = {
    "url": "https://example.com",
    "title": "Example",
    "description": "Example description",
    "category": 1
}


class LinksTestCase(TestCase):
    fixtures = ["categories.json"]

    def test_index(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_link_create(self):
        response = self.client.post("/links/new/", data=EXAMPLE_LINK, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name, ["news/link_list.html"])

    def test_links(self):
        response = self.client.get("/links/")
        self.assertEqual(response.status_code, 200)

    def test_link_update(self):
        self.client.post("/links/new/", data=EXAMPLE_LINK)
        response = self.client.post("/links/1/", data={"title": "New title"})
        self.assertEqual(response.status_code, 200)
