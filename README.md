python-longpoll-example
=======================

A way to do simple (limited number of messages) longpolling in Python using memcache

Requirements:

* webapp2
* requests

Limitations:

* Since all message keys are stored under the channel key, this is only useful for a small number of messages, for instance, running a set of parallel http requests.  Otherwise the size of all the message keys would eventually get too large.  A linked list of message keys would probably work better for a large number of messages.
* Doesn't handle error cases very well
