import http
import json

'''
functions and classes for generating HAR data from parsed http data
'''

# json_repr for HTTP header dicts
def header_json_repr(d):
    return [
        {
            'name': k,
            'value': v
        } for k, v in d.iteritems()
    ]

# add json_repr methods to http classes
def HTTPRequestJsonRepr(self):
    '''
    self = http.Request
    '''
    return {
        'method': self.msg.method,
        'url': self.msg.uri,
        'httpVersion': self.msg.version,
        'cookies': [],
        'queryString': [
            {'name': n, 'value': v}
            for n, v in self.query.values.iteritems()
        ],
        'headersSize': -1,
        'headers': header_json_repr(self.msg.headers),
        'bodySize': len(self.msg.body),
    }
http.Request.json_repr = HTTPRequestJsonRepr

def HTTPResponseJsonRepr(self):
    return {
        'status': self.msg.status,
        'statusText': self.msg.reason,
        'httpVersion': self.msg.version,
        'cookies': [],
        'headersSize': -1,
        'bodySize': len(self.msg.body),
        'redirectURL': self.msg.headers['location'] if 'location' in self.msg.headers else '',
        'headers': header_json_repr(self.msg.headers),
        'content': {
            'size': len(self.msg.body), # should really be uncompressed length
            'mimeType': self.mimeType
        },
    }
http.Response.json_repr = HTTPResponseJsonRepr

# custom json encoder
class JsonReprEncoder(json.JSONEncoder):
    '''
    Custom Json Encoder that attempts to call json_repr on every object it
    encounters.
    '''
    def default(self, obj):
        if hasattr(obj, 'json_repr'):
            return obj.json_repr()
        return json.JSONEncoder.default(self, obj) # should call super instead?