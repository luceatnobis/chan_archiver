#!/usr/bin/env python

class Post(object):

    def __init__(self, **kwarg):

        assert 'no' in kwarg
        for k, v in kwarg.iteritems():
            setattr(self, k, v)

        self.kwarg = kwarg
        self.post_id = int(self.no)

        self._for_abstraction()

    def _for_abstraction(self):
        pass

    def __repr__(self):
        return "<post #%s>" % self.no

    def __str__(self):
        return self.__repr__()

    def __hash__(self):
        return self.post_id

    def __eq__(self, other):
        return self.post_id == other.post_id

class ImagePost(Post):

    def _for_abstraction(self):
        assert 'tim' in self.kwarg
        self.timestamp = int(self.tim)

    def __repr__(self):
        return "%s%s" % (self.tim, self.ext)

    def __str__(self):
        return self.__repr__()

    def __hash__(self):
        return self.timestamp

    def __eq__(self, other):
        return self.timestamp == other.timestamp


if __name__ == "__main__":

    test_data_1 = {'tim': '123', 'ext': 'jpg'}
    test_data_2 = {'tim': '124', 'ext': 'png'}
    test_data_3 = {'tim': '123', 'ext': 'jpg'}

    c = ImagePost(**test_data_1)
    d = ImagePost(**test_data_2)
    e = ImagePost(**test_data_3)

    s = set([c, d, e])
    print s
    print str(s)
