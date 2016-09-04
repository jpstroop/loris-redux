# When compiled, these regexes are just enough to route to the proper
# Handler. The Parameter classes will take care of parsing the arguments and
# making sure they're valid.

# TODO: These should be static. Constantize formats.

# def image_route_pattern(formats=('jpg','png','webp')):
#     path_parts = (
#         # identifier
#         r'/[^/#?@]+',
#         # region
#         r'(?:(?:full|square)|(?:pct:(?:[\d.]+,){3}[\d.]+)|(?:\d+,){3}\d+)',
#         #size
#         r'(?:full|pct:\d+(?:\.\d+)?|,\d+|\d+,|!?\d+,\d+)',
#         # rotation
#         r'(?:!?\d+(?:\.\d+)?)',
#         # quality
#         r'(?:default|color|gray|bitonal)'
#     )
#     fmt = r'\.(?:' + r'|'.join(formats) + r')'
#     return r'(' + r'/'.join(path_parts) + fmt + r')'

def image_route_pattern(formats=('jpg','png','webp')):
    identifier = r'[^/#?@]+'
    params = (
        # region
        r'(?:(?:full|square)|(?:pct:(?:[\d.]+,){3}[\d.]+)|(?:\d+,){3}\d+)',
        #size
        r'(?:full|pct:\d+(?:\.\d+)?|,\d+|\d+,|!?\d+,\d+)',
        # rotation
        r'(?:!?\d+(?:\.\d+)?)',
        # quality
        r'(?:default|color|gray|bitonal)'
    )
    path_parts = r'/'.join(params)
    fmt = r'\.(?:' + r'|'.join(formats) + r')'
    return r'/(' + identifier + r')/(' + path_parts + fmt + r')'

def info_route_pattern():
    return r'/([^/#?@]+)/info.json'

def identifier_route_pattern():
    return r'/([^/#?@]+/?)'
