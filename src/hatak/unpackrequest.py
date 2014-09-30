class UnpackRequest(object):

    def __init__(self):
        self.unpackers = {}

    def add(self, name, method):
        self.unpackers[name] = method

    def __call__(self, obj, request):
        for key, unpacker in self.unpackers.items():
            try:
                value = unpacker(request)
                setattr(obj, key, value)
            except DontUnpackThis:
                pass


def unpack(obj, request):
    obj.request = request
    request.registry['unpacker'](obj, request)


class DontUnpackThis(Exception):
    pass
