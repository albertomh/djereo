from django.test import SimpleTestCase


class IndexViewTest(SimpleTestCase):
    def test_index_returns_200_and_renders_template(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
