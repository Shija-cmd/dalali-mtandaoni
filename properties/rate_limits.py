from functools import wraps

from django.core.cache import cache
from django.shortcuts import render
from rest_framework.response import Response


def get_client_ip(request):

    forwarded_for = request.META.get(
        'HTTP_X_FORWARDED_FOR'
    )

    if forwarded_for:

        return forwarded_for.split(',')[0].strip()

    return request.META.get(
        'REMOTE_ADDR',
        'unknown'
    )


def rate_limit(key_prefix, limit=10, window=300):

    def decorator(view_func):

        @wraps(view_func)
        def wrapped(request, *args, **kwargs):

            key = f'rate-limit:{key_prefix}:{get_client_ip(request)}'
            count = cache.get(
                key,
                0
            )

            if count >= limit:

                if request.path.startswith('/api/'):

                    return Response(
                        {
                            'error': 'Too many attempts. Please try again later.'
                        },
                        status=429
                    )

                return render(
                    request,
                    '429.html',
                    status=429
                )

            if count == 0:

                cache.set(
                    key,
                    1,
                    window
                )

            else:

                cache.incr(
                    key
                )

            return view_func(
                request,
                *args,
                **kwargs
            )

        return wrapped

    return decorator
