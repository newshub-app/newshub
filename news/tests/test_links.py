from django.test import TestCase

INDEX_TITLE = "NewsHub - Collaborative news sharing"
LINKS_TITLE = "NewsHub - Links"
LINK_EDIT_TITLE = "NewsHub - Edit link"
EXAMPLE_LINK_TITLE = "Test link title"
EXAMPLE_LINK = {
    "url": "https://example.com",
    "title": EXAMPLE_LINK_TITLE,
    "description": "Example description",
    "category": 1
}
UPDATED_TITLE = "Modified"


class LinksTestCase(TestCase):
    fixtures = ["categories.json", "admin_user.json"]

    def setUp(self):
        self.client.login(username="admin", password="admin")

    def test_index(self):
        response = self.client.get("/")
        self.assertContains(response, INDEX_TITLE, status_code=200)

    def test_link_create(self):
        response = self.client.post("/links/new/", data=EXAMPLE_LINK, follow=True)
        self.assertContains(response, EXAMPLE_LINK_TITLE, status_code=200)

    def test_links(self):
        response = self.client.get("/links/")
        self.assertContains(response, LINKS_TITLE, status_code=200)

    def test_link_update_get(self):
        self.client.post("/links/new/", data=EXAMPLE_LINK)
        response = self.client.get("/links/1/")
        self.assertContains(response, LINK_EDIT_TITLE, status_code=200)

    def test_link_update_post(self):
        self.client.post("/links/new/", data=EXAMPLE_LINK)
        modified_link = EXAMPLE_LINK.copy()
        modified_link["title"] = UPDATED_TITLE
        response = self.client.post("/links/1/", data=modified_link, follow=True)
        self.assertContains(response, UPDATED_TITLE, status_code=200)
