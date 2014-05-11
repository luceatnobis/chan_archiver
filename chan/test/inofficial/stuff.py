import treq
from twisted.internet import defer, task


urls = [
    'http://example.com',
    'http://example.net',
    'http://example.org',
    'http://example.com',
    'http://example.net',
    'http://example.org',
    'http://example.com',
    'http://example.net',
    'http://example.org',
]

def show_length(response, url):
    """
    def receive_body(body):
        print url, len(body)
    return treq.content(response).addCallback(receive_body)
    """


def main(reactor):
    semaphore = defer.DeferredSemaphore(5)
    deferreds = []
    for url in urls:
        d = semaphore.run(treq.get, url)
        d.addCallback(show_length, url)
        deferreds.append(d)
    return defer.gatherResults(deferreds)


task.react(main, [])
    print response.
