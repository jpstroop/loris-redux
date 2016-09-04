# When compiled, these regexes are just enough to route to the proper
# Handler. The Parameter classes will take care of parsing the arguments and
# making sure they're valid.

# TODO: These should be static. Constantize formats.

def image_route_pattern(formats=('jpg','png','webp')):
    path_parts = (
        r'/([^/#?@]+)', # identifier
        r'((?:full|square)|(?:pct:(?:[\d.]+,){3}[\d.]+)|(?:\d+,){3}\d+)', # region
        r'(full|pct:\d+(?:\.\d+)?|,\d+|\d+,|!?\d+,\d+)',
        r'(!?\d+(?:\.\d+)?)', # rotation
        r'(default|color|gray|bitonal)' # quality
    )
    fmt = r'\.(' + r'|'.join(formats) + r')'
    return r'/'.join(path_parts) + fmt

def info_route_pattern():
    return r'/([^/#?@]+)/info.json'

def identifier_route_pattern():
    return r'/([^/#?@]+/?)'
