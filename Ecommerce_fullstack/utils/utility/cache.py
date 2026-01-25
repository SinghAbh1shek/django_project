from django.core.cache import cache

from django.core.cache import cache

def get_or_set_cache(key, queryset, timeout):
    data = cache.get(key)
    if data is None:
        data = list(queryset)
        cache.set(key, data, timeout)
    return data
