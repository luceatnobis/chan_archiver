#!/usr/bin/env python

import os
import treq
from datetime import datetime

from twisted.internet.defer import DeferredSemaphore

from chan import exceptions, content
from chan import headerstrings as hs

from chan.post import ImagePost
from chan.post_producer import PostProducer
from chan.config_reader import ConfigReader


class Thread(object):

    def __init__(self, thread_url, thread_pool_nr, container_ref, interval=30):

        self.interval = interval
        self.container_ref = container_ref
        self.thread_pool_nr = thread_pool_nr

        self.filenames = set()

        self.folder_tree_built = False
        self.section_dir_settings = "DirectorySettings"
        self.config_reader = ConfigReader()

        self.max_conn = 5  # can of course be changed
        self.semaphore = DeferredSemaphore(self.max_conn)

        self.subfolders = (("html", "content", "thumbs", "misc"))

        self._parse_thread_url(thread_url)
        self.api_url = self._build_json_url()
        self.headers = self._build_header_dict()

    def start(self):
        self._head_request_to_json_api()

    def _set_folders(self):
        """
        This is a working, but cumbersome, way to get construct the folder
        names. I should think of something better at some point.
        """

        config = {
            'root_dir': '~',
            'dump_dir': '4chan'
        }

        config.update(
            self.config_reader.get_section_options(
                self.section_dir_settings))

        for k, v in config.iteritems():
            setattr(self, k, v)

        self.effective_root_dir = os.path.expanduser(self.root_dir)
        self.effective_dump_dir = self.effective_root_dir + os.sep + \
            self.dump_dir + os.sep

        self.board_dir = (self.effective_dump_dir + self.board +
                          os.sep)

        self.thread_dir = self.board_dir + self.chan_thread_id + \
            os.sep

    def _build_folder_tree(self):
        """
        A few words about the eventual layout of the files on the drive, as
        this decision is bound to be made here. I have decided for a layout
        that looks like this:

        There will be a root_dir, its ~ per default. In root_dir there will
        be a dump_dir, which serves to limit the entire dumping process in one
        folder. The default for dump_dir is 4chan/. In this dump_dir there
        will be olders for each board. If a board folder is not present when
        a thread from the board is to be dumped, it will be created. We shall
        call this folder board_dir, for example ~/4chan/wg.

        A thread will be dumped into board_dir with a folder name of the
        respective thread number.

        This will be the thread_dir, ~/4chan/wg/5764713.

        Now, there are a few things that need to be stored here:

            a) the actual images
            b) the thumbnails
            c) the html
            d) the stylesheet
            e) the "top image" for style.


        Because I don't want to have hard drive access every time because the
        existence of the folder tree needs to be checked, the creation of it
        will happen here.
        """

        self._set_folders()

        for f in self.subfolders:
            full_path = self.thread_dir + f
            if not os.path.exists(full_path):
                os.makedirs(full_path)

            setattr(self, "%s_dir" % (f), full_path)
            self.folder_tree_built = True

    def _build_header_dict(self):
        return {'User-Agent': hs.useragent_ff}

    def _build_time_stamp(self):
        return datetime.utcnow().strftime("%a, %d %b %Y %T GMT")

    def _update_header_dict(self):
        self.headers['If-Modified-Since'] = self._build_time_stamp()

    def _parse_thread_url(self, thread_url):
        """
        We will parse the URL into these components (usefulness may vary):
        protocol        :   http/https (https preferred!)
        board           :   the board that the thread is in
        chan_thread_id :   the unique ID that every post (and thread) gets

        A thread might have a "title" in the URL next to thread id. It will
        be stripped as it serves no purpose to either identifying a thread to
        4chan nor does it prove useful for any of our local purposes so it
        will simply get left out.

        Exceptions may be thrown at will.
        """

        self.thread_url = thread_url
        split = [x for x in thread_url.split("/") if x]
        try:
            self.protocol = split[0][:-1]  # removes the :
            self.board = split[2]
            self.chan_thread_id = split[4]
        except IndexError:
            exception_str = "Could not parse \"%s\"" % thread_url
            raise exceptions.URLParsingFailed(exception_str)

    def _build_json_url(self):
        """
        This will build the URL to the JSON API on 4chan that describes
        the contents of a thread.
        """

        return "%s://a.4cdn.org/%s/thread/%s.json" % (
            self.protocol, self.board, self.chan_thread_id)

    def _head_request_to_json_api(self):
        """
        This is the initial request which checks whether the json document
        is even online anymore; during the interval, a lot can happen to the
        thread, most notably of all, it could 404. A head request to the json
        document keeps the overhead minimal as possible as the check whether
        a download of the json data is necessary depends on the headers.

        In the first run we don't pass the 'If-Modified-Since' header to the
        server since we didn't run it before. On all runs it needs to be
        updated before the LoopingCall starts again, that is,

        a) after the first run is finished and the thread exists
        b) in all continuous runs after the head request and the thread exists
        """

        d = treq.head(self.api_url, headers=self.headers)
        d.addCallback(self._head_request_to_json_api_success)
        d.addErrback(self._json_failure)

    def _json_failure(shit):

        print shit

    def _head_request_to_json_api_success(self, response):
        """
        This only means that the request itself went well, it says nothing
        about the state of the headers.
        """

        if response.code == 304:  # Nothing changed, do nothing I guess
            print "304"
            pass
        elif response.code == 404:  # Its dead
            uri = response.original.request.absoluteURI
            print "Received %s for %s, unregistering now." % (
                response.code, uri)

            self._handle_not_found()  # now I CAN unregister it here <3
        elif response.code == 200:  # it was found fine
            self._fetch_json_data()

    def _fetch_json_data(self):
        """
        Here I will fetch the json data for this very thread and do
        find a) the thumbnails b) the content c) the html document,
        download them and hopefully store them.

        It is also very likely, and I think necessary, that this function
        does kick in a huge amount of deferreds.

        Oh well.
        """

        d = treq.get(self.api_url, headers=self.headers)
        d.addCallback(self._fetch_json_thread_headers_success)
        d.addErrback(self._fetch_json_thread_headers_failure)

    def _fetch_json_thread_headers_success(self, result):
        """
        Here will I arrive when fetching the json information has been
        successful and the body needs to be retrieved. treq.text_content does
        that for us, that has to do with the API of Agents.
        """

        json_url = result.request.original.uri
        d = treq.text_content(result)
        d.addCallback(self._fetch_json_thread_body_success, json_url)

    def _fetch_json_thread_headers_failure(failure):
        """
        Needs to print the exception and cancel the LoopingCall responsible
        for this thread at this point as a pretty severe error was received.
        """
        print failure

    def _fetch_json_thread_body_success(self, result, uri):
        """
        The json was successfully retrieved and we do a few things here:

        a)  we store the json content and decode it to a json object.
        b)  we parse it for all images and manage to download them.
        c)  we also notice that the thread is indeed alive, therefore we
            register a LoopingCall .
        d)  we update the self.headers object to include the If-Modified-Since
            header field; from this point on, we want to communicate with
            metadata only.
        e)  we will create the folder tree at this point
        f)  the json content lives on as, when the thread has 404'd, we can
            generate a backup of the HTML content, but thats a bit in the
            future at this point.
        """

        if len(result) == 0:
            print "Bad JSON received; restarting in %s seconds" % (
                self.container_ref.restart_delay)
            self.container_ref.restart_delayed(self)
            return

        post_producer_info = {
            'protocol': self.protocol,
            'board': self.board,
            'id': self.chan_thread_id
            }

        post_producer = PostProducer(result, **post_producer_info)

        """
        if not self.folder_tree_built:
            self._build_folder_tree()
        """

        new_posts = set(post_producer.posts_with_images_wrapped())
        difference = new_posts - self.filenames

        # TODO: Kick off routines to download stuff

        self.filenames.update(new_posts)

        if not self._check_loopingcall_registered():
            self._register_loopingcall()

        self._update_header_dict()

    def _handle_not_found(self):
        self._remove_loopingcall()

    def _check_loopingcall_registered(self):
        return self.thread_pool_nr in self.container_ref.loopingcalls

    def _register_loopingcall(self):
        """
        Registers the LoopingCall at the responsible ThreadContainer object
        which we have the self.container_ref for.
        """

        self.container_ref.add_loopingcall(self)

    def _remove_loopingcall(self):
        """
        This is a function to remove the thread from the list of active
        threads. I do plan to implement LoopingCalls, so I don't delete an
        object from the dictionary but cancel a LoopingCall which is referenced
        by a LoopingCall and an ID.

        Its complicated. But not really.
        """

        self.container_ref.remove_loopingcall(self)


def thread(thread_url, ref, thread_pool_nr, interval=30):
    return Thread(thread_url, ref, thread_pool_nr, interval=interval)
