from django.test.runner import DiscoverRunner
from django.test.utils import override_settings


class TestRunner(DiscoverRunner):
    """Custom test runner to apply test-specific settings.

    Override per-test with the following decorator:
    ```
    @override_settings(DEBUG=False)
    def test_unit(self):
        ...
    ```
    """

    def run_tests(self, *args, **kwargs):
        with override_settings(**TEST_SETTINGS):
            return super().run_tests(*args, **kwargs)


TEST_SETTINGS = {
    "DEBUG": False,
}
