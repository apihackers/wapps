from wagtail.wagtailcore.models import Page

from . import social
from .models import IdentitySettings


def website(context):
    request = context['request']
    site = request.site
    identity = IdentitySettings.for_site(site)
    return {
        "@type": "WebSite",
        "name": site.site_name,
        "alternateName": identity.description,
        "keywords": ','.join(t.name for t in identity.tags.all()),
        "url": site.root_url,
    }


def site_navigation(context):
    return [{
        "@type": "SiteNavigationElement",
        "name": page.title,
        "url": page.full_url
    } for page in Page.objects.live().in_menu().filter(depth__lte=3)]


def breadcrumb(context):
    if 'page' not in context:
        return
    page = context['page']
    elements = []
    for parent in page.get_ancestors():
        if parent.is_root():
            continue
        elements.append({
            "@type": "ListItem",
            "position": len(elements) + 1,
            "item": {
                "@id": parent.full_url,
                "name": parent.title,
            }
        })
    elements.append({
        "@type": "ListItem",
        "position": len(elements) + 1,
        "item": {
            "@id": page.full_url,
            "name": page.title,
        }
    })
    return {
        "@type": "BreadcrumbList",
        "itemListElement": elements
    }


def organization(context):
    request = context['request']
    site = request.site
    identity = IdentitySettings.for_site(site)
    org = {
        "@type": "Organization",
        "address": [
            {
                "@type": "PostalAddress",
                "addressLocality": "Paris, France",
            },
            {
                "@type": "PostalAddress",
                "addressLocality": "Melun, France",
            }
        ],
        "url": site.root_url,
        # "email": "lesly(at)lamarieesublimee.fr",
        # "founder": {
        #     "@type": "Person",
        #     "name": "Lesly T."
        # },
        "name": identity.name,
    }
    if identity.logo:
        org['logo'] = site.root_url + identity.logo.get_rendition('original').url
    same_as = []
    for network in social.NETWORKS.keys():
        username = getattr(identity, network, None)
        if username and 'url' in social.NETWORKS[network]:
            network_url = social.user_url(network, username)
            same_as.append(network_url)
    if same_as:
        org['sameAs'] = same_as
    return org


def add_to_graph(graph, data):
    if isinstance(data, dict):
        graph.append(data)
    elif isinstance(data, (list, tuple)):
        graph.extend(data)


def graph(context, *data):
    graph = [
        website(context),
    ]
    add_to_graph(graph, breadcrumb(context))
    add_to_graph(graph, organization(context))
    add_to_graph(graph, site_navigation(context))

    for d in data:
        if d and hasattr(d, '__jsonld__'):
            add_to_graph(graph, d.__jsonld__(context))

    return {
        "@context": 'http://schema.org/',
        "@graph": graph,
    }
