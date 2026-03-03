class SecurityHeadersMiddleware:
    # Tests exist in `SecurityHeadersMiddlewareTests`, but coverage fails to detect this,
    # hence the pragma directives.
    def __init__(self, get_response):  # pragma: no cover
        self.get_response = get_response

    def __call__(self, request):  # pragma: no cover
        response = self.get_response(request)

        # 'Cross-Origin-Opener-Policy' has default "same-origin"
        # this isolates browser window from cross-origin documents
        # <https://docs.djangoproject.com/en/6.0/ref/settings/#secure-cross-origin-opener-policy>

        # prevents your document from loading any cross-origin resources
        # (unless explicitly permitted via a CORP header)
        response["Cross-Origin-Embedder-Policy"] = "require-corp"
        # prevents the document from being loaded by cross-origin resources
        response["Cross-Origin-Resource-Policy"] = "same-origin"

        return response
