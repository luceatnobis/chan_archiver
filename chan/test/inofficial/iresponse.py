#!/usr/bin/env python

from twisted.web.iweb import IResponse

def main():

    r = IResponse
    print dir(r)

main()
