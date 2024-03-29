class TTLProcessor(object):
    """
    Middleware to dynamically attach Varnish Cache headers to response by rendering url.
    """
    DONT_CACHE = 0
    THIRTY_SECONDS = 30
    ONE_MINUTE = 60
    TWO_MINUTES = 60 * 2
    FIVE_MINUTES = 60 * 5
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
            response['Cache-Control'] = TTLProcessor.__get_cache_control(request.path, request.resolver_match.url_name)


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
            # Low-Level Cache
            'video-detail': TTLProcessor.FIVE_MINUTES,
            # Mid-Level Cache Endpoints
            '/api/v1/search/trending/': TTLProcessor.THIRTY_MINUTES,
            '/api/v1/search/trendsetters/': TTLProcessor.THIRTY_MINUTES,
            '/api/v1/search/': TTLProcessor.ONE_HOUR,
            '/api/v1/search/explore/': TTLProcessor.ONE_HOUR,
            '/api/v1/search/ranked10/': TTLProcessor.ONE_HOUR,
            '/api/v1/videos/top/': TTLProcessor.ONE_HOUR,

            # Long lived responses
            '/api/v1/categories/': TTLProcessor.ONE_DAY,

            # Will need to purge early - but for now won't cache.
            'profile-following': TTLProcessor.DONT_CACHE,
            'profile-followers': TTLProcessor.DONT_CACHE,
            'profile-detail': TTLProcessor.THIRTY_SECONDS,
        }

        time = resolver_mapper.get(raw_path, None) or resolver_mapper.get(url_name, None)
        if not time:
            time = TTLProcessor.DONT_CACHE

        return time

    @staticmethod
    def __get_cache_control(raw_path, url_name):
        # Cache-Control Mapper
        resolver_mapper = {
            # No Cache Endpoints
            'default': TTLProcessor.DONT_CACHE,
            '/api/v1/josh/': TTLProcessor.DONT_CACHE,
            '/api/v1/videos/': TTLProcessor.DONT_CACHE,
            '/api/v1/users/me/': TTLProcessor.DONT_CACHE,
            # Low-Level Cache
            'video-detail': TTLProcessor.FIVE_MINUTES,
            # Mid-Level Cache Endpoints
            '/api/v1/search/trending/': TTLProcessor.THIRTY_MINUTES,
            '/api/v1/search/trendsetters/': TTLProcessor.THIRTY_MINUTES,
            '/api/v1/search/': TTLProcessor.ONE_HOUR,
            '/api/v1/search/explore/': TTLProcessor.ONE_HOUR,
            '/api/v1/search/ranked10/': TTLProcessor.ONE_HOUR,
            '/api/v1/videos/top/': TTLProcessor.ONE_HOUR,

            # Long lived responses
            '/api/v1/categories/': TTLProcessor.ONE_DAY,

            # Will need to purge early - but for now won't cache.
            'profile-following': TTLProcessor.DONT_CACHE,
            'profile-followers': TTLProcessor.DONT_CACHE,
            'profile-detail': TTLProcessor.THIRTY_SECONDS,
        }

        age = resolver_mapper.get(raw_path, None) or resolver_mapper.get(url_name, None)
        if not age:
            age = TTLProcessor.DONT_CACHE

        return 'max-age={}'.format(age)