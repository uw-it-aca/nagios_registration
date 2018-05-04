from django.http import HttpResponse
from oauth_provider.utils import get_oauth_request, verify_oauth_request
from oauth_provider.store import store, InvalidConsumerError, InvalidTokenError
from functools import wraps
from django.conf import settings


def authenticate_application(func):
    def _wrapper(*args, **kwargs):
        request = args[0]
        try:
            oauth_request = get_oauth_request(request)
            if (oauth_request is None):
                raise ValueError('No Oauth Request')
            consumer = store.get_consumer(request,
                                          oauth_request,
                                          oauth_request['oauth_consumer_key']
                                          )
            verify_oauth_request(request, oauth_request, consumer)
            request.META['OAUTH_CONSUMER_NAME'] = consumer.name
            request.META['OAUTH_CONSUMER_PK'] = consumer.pk
            return func(*args, **kwargs)
        except ValueError as e:
            if login_auth(request):
                return func(*args, **kwargs)
            else:
                response = HttpResponse("Error authorizing user login")
                response.status_code = 401
        except Exception as e:
            print "Error: ", e
            response = HttpResponse("Error authorizing application with OAUTH")
            response.status_code = 401
        return response

    return wraps(func)(_wrapper)


def login_auth(request):
    try:
        return (request.user.is_authenticated() and
                request.user.username in settings.AUTHORIZED_USERS)
    except Exception as e:
        print e
        return False
