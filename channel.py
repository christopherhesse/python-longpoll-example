import pylibmc
import time
import hashlib
import os


TIMEOUT = 30


def get_mc():
    return pylibmc.Client(['localhost:11211'])


def create():
    """
    Create a channel for reading/writing messages
    """
    mc = get_mc()
    # create the channel key so that we can append to it later
    channel_key = hashlib.sha1(os.urandom(32)).hexdigest()
    mc.set(channel_key, '')
    # the next key starts at index 0
    return channel_key + ':0'


def write(key, message):
    """
    Write a single message to a channel
    """
    channel_key, _message_index = str(key).split(':')
    mc = get_mc()
    message_key = hashlib.sha1(message).hexdigest()
    mc.set(message_key, message)
    mc.append(channel_key, ',' + message_key)


def read(key, timeout=TIMEOUT):
    """
    Read the next message from the channel specified by the key
    """
    channel_key, result_index = str(key).split(':')
    result_index = int(result_index)

    mc = get_mc()
    # check channel_key for new results, if new ones are found, return them to the user
    start_time = time.time()
    while time.time() - start_time < TIMEOUT:
        channel_contents = mc.get(channel_key)
        if channel_contents:
            result_keys = channel_contents.split(',')
            if len(result_keys) > result_index + 1:
                result_index += 1
                message = mc.get(result_keys[result_index])
                next_key = channel_key + ':' + str(result_index)
                return next_key, message
        # poll every 200ms
        time.sleep(0.2)

    return None, None
