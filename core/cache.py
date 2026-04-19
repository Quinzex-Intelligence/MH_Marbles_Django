import functools
from django.core.cache import cache
from django.utils.encoding import force_bytes
from django.conf import settings
from rest_framework.response import Response

DEFAULT_CACHE_TIMEOUT = 3600  # 1 hour

def get_model_version_key(model_name):
    """Generates a key for tracking the cache version of a model."""
    return f"cache_version_{model_name}"

def get_model_version(model_name):
    """Gets the current cache version for a model."""
    version_key = get_model_version_key(model_name)
    version = cache.get(version_key)
    if version is None:
        version = 1
        cache.set(version_key, version, timeout=None)
    return version

def clear_model_cache(model_name):
    """
    Invalidates all cache for a model by bumping its version.
    This is extremely efficient in Redis using incr.
    """
    version_key = get_model_version_key(model_name)
    try:
        cache.incr(version_key)
    except ValueError:
        # If key doesn't exist, set it to 1
        cache.set(version_key, 1, timeout=None)

def get_cache_key(model_name, action, detail_id=None, extra=None):
    """
    Generates a versioned cache key.
    Example: cache_v1_product_list_category=1
    """
    version = get_model_version(model_name)
    key = f"cache_v{version}_{model_name}_{action}"
    if detail_id:
        key += f"_{detail_id}"
    if extra:
        key += f"_{extra}"
    return key

def cache_response(model_name, timeout=DEFAULT_CACHE_TIMEOUT):
    """
    Decorator for FBVs to cache responses and handle invalidation via versioning.
    Usage: @cache_response('company')
    """
    def decorator(view_func):
        @functools.wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Only cache GET requests
            if request.method != 'GET':
                response = view_func(request, *args, **kwargs)
                # If it's a write operation, bump the version to invalidate cache
                if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
                    if 200 <= response.status_code < 300:
                        clear_model_cache(model_name)
                return response

            # Check if this is a detail view (has ID in kwargs)
            detail_id = None
            for key in ['id', 'company_id', 'collection_id', 'pk']:
                if key in kwargs:
                    detail_id = kwargs[key]
                    break
            
            # Simple action identification
            action = 'list' if detail_id is None else 'retrieve'
            
            # Include query params for list views
            extra = None
            if action == 'list':
                extra = request.query_params.urlencode()
            
            cache_key = get_cache_key(model_name, action, detail_id, extra)
            cached_data = cache.get(cache_key)
            
            if cached_data is not None:
                return Response(cached_data)
            
            response = view_func(request, *args, **kwargs)
            
            if isinstance(response, Response) and response.status_code == 200:
                cache.set(cache_key, response.data, timeout)
                
            return response
        return _wrapped_view
    return decorator

class RedisCacheMixin:
    """
    Mixin for ViewSets to handle automatic versioned caching and invalidation.
    """
    cache_timeout = DEFAULT_CACHE_TIMEOUT

    def get_model_name(self):
        if hasattr(self, 'queryset') and self.queryset is not None:
            return self.queryset.model._meta.model_name
        if hasattr(self, 'get_queryset'):
            qs = self.get_queryset()
            if qs is not None:
                return qs.model._meta.model_name
        return self.__class__.__name__.lower()

    def dispatch(self, request, *args, **kwargs):
        model_name = self.get_model_name()
        
        # For write operations, clear cache AFTER the operation
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            response = super().dispatch(request, *args, **kwargs)
            if 200 <= response.status_code < 300:
                clear_model_cache(model_name)
            return response
            
        return super().dispatch(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        model_name = self.get_model_name()
        # include query params in cache key to handle filtering/pagination
        query_params = request.query_params.urlencode()
        cache_key = get_cache_key(model_name, 'list', extra=query_params)
        
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return Response(cached_data)
            
        response = super().list(request, *args, **kwargs)
        if response.status_code == 200:
            cache.set(cache_key, response.data, self.cache_timeout)
        return response

    def retrieve(self, request, *args, **kwargs):
        model_name = self.get_model_name()
        pk = kwargs.get('pk')
        cache_key = get_cache_key(model_name, 'retrieve', pk)
        
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return Response(cached_data)
            
        response = super().retrieve(request, *args, **kwargs)
        if response.status_code == 200:
            cache.set(cache_key, response.data, self.cache_timeout)
        return response
