from django import template

from contest import util

register = template.Library()

@register.inclusion_tag('contest/sc_widget.html')
def sc_widget(sc_url):
    """ All the options:
        https://github.com/soundcloud/Widget-JS-API/wiki/widget-options
    """
    base_url = "http://player.soundcloud.com/player.swf"
    params = {
            'url': sc_url,
            'auto_play': 'false',
            'show_user': 'false',
            'show_playcount': 'false',
            'show_comments': 'false',
            'show_artwork': 'false',
            'color': '550055',#'ff6600', # 444444
            'font': 'Arial',
            }

    if False:
        params['player_type'] = 'tiny'
        height = 18
    else:
        height = 81
        params.update({
            'sharing': 'false',
            'download': 'false'
            })

    full_url = base_url + '?' + '&amp;'.join([key + '=' + value for (key, value) in params.iteritems()])
    return {'height': height, 'type': 'flash', 'widget_url': full_url}


@register.inclusion_tag('contest/sc_connect.html')
def sc_connect():
    sc_client = util.get_soundcloud_client()
    return {'url': sc_client.authorize_url()}
