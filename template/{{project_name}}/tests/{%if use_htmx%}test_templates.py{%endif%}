import ast

from bs4 import BeautifulSoup
from django.test import Client, SimpleTestCase


class HtmxTest(SimpleTestCase):
    def setUp(self):
        self.client = Client()

    def test_body_has_htmx_csrftoken_header(self):
        res = self.client.get("/")
        html = BeautifulSoup(res.content)
        body = html.find("body")
        try:
            hx_headers = body.attrs["hx-headers"]
            hx_headers_val = ast.literal_eval(hx_headers)
            x_csrftoken = hx_headers_val["X-CSRFToken"]
            self.assertEqual(len(x_csrftoken), 64)
        except KeyError:
            self.fail("No 'hx-headers' attribute found on <body> when one was expected")
