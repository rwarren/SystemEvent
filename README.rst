Introduction
============

``SystemEvent`` provides a simple synchronization primitive for use across multiple
processes. The ``SystemEvent`` object emulates the ``threading.Event`` API exactly. In
addition, simple scripts (``evt_set``, ``evt_wait``, and ``evt_clear``) are installed for
easy usage from shell scripts.

The main reason to use ``SystemEvent`` is in situations when you want processes to wait
on other processes without the need for polling.

Installation
============

``pip install SystemEvent``

Usage
=====

``SystemEvent`` uses named posix semaphores under the hood, so you need to choose event
names that are unique to your application. Any event references will use this unique name.

From Python, use it *exactly* like you would use a ``threading.Event`` instances, with the
main difference being that you need to give your event a name so that other processes can
reference it.

For example, in as many consoles as you like, set up an event and have it wait (the last
line will block on each ```wait()`` call):

    >>> import SystemEvent
    >>> evt = SystemEvent.SystemEvent("my_event")
    >>> evt.wait()

Alternatively, you can just run ``evt_wait my_event`` from your favorite shell (this is
just a small script that does the above almost exactly).

In another console, set the event and note that the first event releases:

    >>> import SystemEvent
    >>> evt = SystemEvent.SystemEvent("my_event")
    >>> evt.set()

All events blocking on "my_event" will be immediately released by this ``set()`` call.
Subsequent calls to ``evt.wait()`` from any process will not block, since the event is now
globally latched.

To clear the event (so that calls to ``evt.wait()`` will block again), call
``evt.clear()``.

As with ``threading.Event`` (and ``multiprocessing.Event``) there is also an ``isSet()``
method which tells you the current state (but watch out for race conditions when checking
it).

Shell scripts
=============

Three shell scripts are provided, with the following usage:

    evt_wait <event_name> [timeout_s]

    evt_set <event_name>

    evt_clear <event_name>

These scripts are thin shells over ``SystemEvent`` usage. The ``timeout_s`` option on
``evt_wait`` is optional, and defaults to infinity.

All scripts have an exit code of 0, unless ``evt_wait`` times out, in which case it
returns 1.

How does it work?
=================

``SystemEvent`` currently uses a posix semaphore internally. To integrate with other
non-python applications, you can just access the same named semaphore. Just be careful
that you increment and decrement correctly. Check out the code for details... it is
ridiculously small.

License
=======
MIT.  See ``LICENSE`` file.

TODO
====

1. Add tests
2. Make it work in Windows, too
3. Remove the ``posix_ipc`` requirement

