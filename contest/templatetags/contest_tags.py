from django import template 

register = template.Library()

@register.inclusion_tag('contest/sc_widget.html')
def sc_widget(sc_url):
    return {'sc_url': sc_url, 'type': 'tiny_flash'}
