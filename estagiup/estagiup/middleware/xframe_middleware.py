class XFrameOptionsExemptMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # Se a URL for a de tutoriais, apaga o cabeçalho problemático
        if request.path.strip('/') == 'tutoriais':
            if 'X-Frame-Options' in response.headers:
                del response.headers['X-Frame-Options']
        return response