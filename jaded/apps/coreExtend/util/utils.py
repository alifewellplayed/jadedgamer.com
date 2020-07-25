import functools
import hashlib

try:
    from urlparse import urlunparse
except ImportError:
    from urllib.parse import urlunparse

from django.conf import settings
from django.utils.http import is_safe_url
from django.contrib.sites.models import Site
from django.urls import reverse as simple_reverse


def generate_secret_token(phrase, size=12):
    """Generate a (SHA1) security hash from the provided info."""
    info = "".join([phrase, settings.SECRET_KEY])
    return hashlib.sha1(info.encode("utf-8")).hexdigest()[:size]


def current_site_domain():
    if settings.SITE_URL == "http://localhost":
        domain = "http://localhost"
    else:
        domain = Site.objects.get_current().domain
        prefix = "www."
        if getattr(settings, "REMOVE_WWW_FROM_DOMAIN", False) and domain.startswith(prefix):
            domain = domain.replace(prefix, "", 1)
    return domain


get_domain = current_site_domain


def get_redirect_url(request):
    redirect_to = request.POST.get("next", request.GET.get("next", ""))
    url_is_safe = is_safe_url(
        url=redirect_to, allowed_hosts=set(request.get_host()), require_https=request.is_secure(),
    )
    return redirect_to if url_is_safe else ""


def urljoin(domain, path=None, scheme=None):
    """
    Joins a domain, path and scheme part together, returning a full URL.

    :param domain: the domain, e.g. ``example.com``
    :param path: the path part of the URL, e.g. ``/example/``
    :param scheme: the scheme part of the URL, e.g. ``http``, defaulting to the
        value of ``settings.DEFAULT_URL_SCHEME``
    :returns: a full URL
    """
    if scheme is None:
        scheme = getattr(settings, "DEFAULT_URL_SCHEME", "http")

    return urlunparse((scheme, domain, path or "", None, None, None))


def reverse(viewname, subdomain=None, scheme=None, args=None, kwargs=None, current_app=None):
    """
    Reverses a URL from the given parameters, in a similar fashion to
    :meth:`django.urls.reverse`.

    :param viewname: the name of URL
    :param subdomain: the subdomain to use for URL reversing
    :param scheme: the scheme to use when generating the full URL
    :param args: positional arguments used for URL reversing
    :param kwargs: named arguments used for URL reversing
    :param current_app: hint for the currently executing application
    """
    urlconf = settings.SUBDOMAIN_URLCONFS.get(subdomain, settings.ROOT_URLCONF)

    domain = get_domain()
    if subdomain is not None:
        domain = "%s.%s" % (subdomain, domain)

    path = simple_reverse(viewname, urlconf=urlconf, args=args, kwargs=kwargs, current_app=current_app)
    return urljoin(domain, path, scheme=scheme)


#: :func:`reverse` bound to insecure (non-HTTPS) URLs scheme
insecure_reverse = functools.partial(reverse, scheme="http")

#: :func:`reverse` bound to secure (HTTPS) URLs scheme
secure_reverse = functools.partial(reverse, scheme="https")

#: :func:`reverse` bound to be relative to the current scheme
relative_reverse = functools.partial(reverse, scheme="")
