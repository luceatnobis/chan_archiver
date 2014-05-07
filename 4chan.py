#!/usr/bin/env python

import argparse
from twisted.internet import reactor
from twisted.web.client import Agent, CookieAgent

from chan.threadcontainer import ThreadContainer

def main():
    
    c = ThreadContainer()
    parser = argparse.ArgumentParser()
    
    parser.add_argument("thread", nargs="+", )
    parser.add_argument("-t", "--interval", type=int, default=30)
    parser.add_argument("-r", default=False, action="store_true")

    args = parser.parse_args()

    for t in set(args.thread):
        c.add_thread(t, interval=args.interval)

    if args.r:
        reactor.run()

if __name__ == "__main__":
    main()
