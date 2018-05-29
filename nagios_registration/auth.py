from django.http import HttpResponse
from django.conf import settings
from oauth_provider.utils import get_oauth_request, verify_oauth_request
from oauth_provider.store import store, InvalidConsumerError, InvalidTokenError
from uw_saml.decorators import group_required
from uw_saml.utils import is_member_of_group


def authenticate_application(func):
    def wrapper(request, *args, **kwargs):
        try:
            oauth_request = get_oauth_request(request)
            if (oauth_request is None):
                raise ValueError('No Oauth Request')
            consumer = store.get_consumer(
                request, oauth_request, oauth_request['oauth_consumer_key'])
            verify_oauth_request(request, oauth_request, consumer)
            request.META['OAUTH_CONSUMER_NAME'] = consumer.name
            request.META['OAUTH_CONSUMER_PK'] = consumer.pk
            return func(request, *args, **kwargs)
        except ValueError as e:
            if is_member_of_group(request, settings.NAGIOS_ADMIN_GROUP):
                return func(request, *args, **kwargs)
            return HttpResponse("Access Denied", status_code=401)
        except (InvalidConsumerError, InvalidTokenError) as e:
            return HttpResponse("Access Denied", status_code=401)

    return wrapper
