import webapp2
import requests
import json
import re
from multiprocessing.pool import ThreadPool

import channel

BASE_URL = 'https://twitter.com/'


def get_last_tweet(key, handle):
    content = requests.get(BASE_URL + handle).content
    content = re.sub(r'\s+', ' ', content)
    start_index = content.find('<p class="js-tweet-text">')
    end_index = content.find('</p>', start_index)
    content = content[start_index:end_index]
    content = re.sub(r'<.*?>', '', content)
    channel.write(key, content)


class TwitterFetcher(webapp2.RequestHandler):
    def get(self):
        key = self.request.get('key')
        if key:
            next_key, result = channel.read(key)
            response = json.dumps(dict(
                next_key=next_key,
                result=result,
            ))
            self.response.write(response)
            return

        handles = self.request.get_all('handles')
        key = channel.create()
        pool = ThreadPool(len(handles))
        pool.map_async(lambda handle: get_last_tweet(key, handle), handles)
        response = dict(next_key=key)
        self.response.write(json.dumps(response))


app = webapp2.WSGIApplication([
    (r'/fetch_twitter', TwitterFetcher),
], debug=True)


def main():
    from wsgiref import simple_server
    server = simple_server.WSGIServer(('127.0.0.1', 8080), simple_server.WSGIRequestHandler)
    server.set_app(app)
    server.serve_forever()


if __name__ == '__main__':
    main()
