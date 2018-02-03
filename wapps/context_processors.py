from django.conf import settings


def google(request):
    return {
        'GOOGLE_API_KEY': getattr(settings, 'GOOGLE_API_KEY', None),
        'GOOGLE_ANALYTICS_ID': getattr(settings, 'GOOGLE_ANALYTICS_ID', None),
    }


def config(request):
    return {
        'WAGTAIL_SITE_NAME': getattr(settings, 'WAGTAIL_SITE_NAME', None),
    }
