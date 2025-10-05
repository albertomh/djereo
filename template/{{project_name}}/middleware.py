class SecurityHeadersMiddleware:
    # Tests exist in `SecurityHeadersMiddlewareTests`, but coverage fails to detect this,
    # hence the pragma directives.
    def __init__(self, get_response):  # pragma: no cover
        self.get_response = get_response

    def __call__(self, request):  # pragma: no cover
        response = self.get_response(request)

        response["Cross-Origin-Embedder-Policy"] = "require-corp"
        response["Cross-Origin-Resource-Policy"] = "same-origin"

        return response
