class TTLProcessor(object):
    """
    Middleware to dynamically attach Varnish Cache headers to response by rendering url.
    """
    DONT_CACHE = 0
    ONE_MINUTE = 60
    TWO_MINUTES = 60 * 2
    THIRTY_MINUTES = 60 * ONE_MINUTE
    ONE_HOUR = ONE_MINUTE * 60
    ONE_DAY = ONE_HOUR * 24
    ONE_WEEK = ONE_DAY * 7

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.__process_response(request)


    def __process_response(self, request):
        """
        :type request: django.core.handlers.wsgi.WSGIRequest
        :type response: Response or HttpResponse
        :return: Response or HttpResponse
        """
        # Pull the url resolver name from the django url route # ex: video-list, video-detail etc
        response = self.get_response(request)

        try:
            response['X-CACHE-TTL'] = TTLProcessor.__get_cache_timeout(request.path, request.resolver_match.url_name)
            return response
        except AttributeError:
            # Catches requests to /admin - Django doesn't attach a resolver attribute to it.
            return response

    @staticmethod
    def __get_cache_timeout(raw_path, url_name):
        # TTL Mapper
        resolver_mapper = {
            # No Cache Endpoints
            'default': TTLProcessor.DONT_CACHE,
            '/api/v1/josh/': TTLProcessor.DONT_CACHE,
            '/api/v1/videos/': TTLProcessor.DONT_CACHE,
            '/api/v1/users/me/': TTLProcessor.DONT_CACHE,
            # Mid-Level Cache Endpoints
            '/api/v1/search/trending/': TTLProcessor.THIRTY_MINUTES,
            '/api/v1/search/trendsetters/': TTLProcessor.THIRTY_MINUTES,
            '/api/v1/search/': TTLProcessor.ONE_HOUR,
            '/api/v1/search/explore/': TTLProcessor.ONE_HOUR,
            '/api/v1/search/ranked10/': TTLProcessor.ONE_HOUR,
            '/api/v1/videos/top/': TTLProcessor.ONE_HOUR,

            # Long lived responses
            '/api/v1/categories/': TTLProcessor.ONE_DAY,

            # Will need to purge early.
            'profile-following': TTLProcessor.ONE_HOUR,
            'profile-followers': TTLProcessor.ONE_HOUR,
            'profile-detail': TTLProcessor.ONE_HOUR,
            'video-detail': TTLProcessor.TWO_MINUTES
        }

        time = resolver_mapper.get(raw_path, None) or resolver_mapper.get(url_name, None)
        if not time:
            time = TTLProcessor.DONT_CACHE

        return time