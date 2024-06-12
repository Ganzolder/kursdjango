from django.core.cache import cache

from config.settings import CACHE_ENABLED
from main.models import Post


def get_posts_from_cache():
    if not CACHE_ENABLED:
        return Post.objects.all()
    key = 'post_list'
    posts = cache.get(key)
    if posts is not None:
        return posts
    posts = Post.objects.all()

    cache.set(key, posts)

    return posts
