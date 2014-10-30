from django.http import HttpResponse
from oauth_provider.utils import get_oauth_request, verify_oauth_request
from oauth_provider.store import store, InvalidConsumerError, InvalidTokenError
from functools import wraps


def authenticate_application(func):
    def _wrapper(*args, **kwargs):
        request = args[0]
        try:
            oauth_request = get_oauth_request(request)
            consumer = store.get_consumer(request,
                                          oauth_request,
                                          oauth_request['oauth_consumer_key']
                                          )
            verify_oauth_request(request, oauth_request, consumer)
            request.META['OAUTH_CONSUMER_NAME'] = consumer.name
            request.META['OAUTH_CONSUMER_PK'] = consumer.pk
            return func(*args, **kwargs)
        except Exception as e:
            print "Error: ", e
            response = HttpResponse("Error authorizing application")
            response.status_code = 401
        return response

    return wraps(func)(_wrapper)
