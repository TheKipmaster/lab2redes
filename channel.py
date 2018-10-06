class Channel:
    def __init__(self, name):
        self.name = name
        self.clients = {}

    def __repr__(self):
        return "<Channel name:%s clients:%s>" % (self.name, self.clients)

    def __str__(self):
        return "From str method of Channel: a is %s, b is %s" % (self.name, self.clients)