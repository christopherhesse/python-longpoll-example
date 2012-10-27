import requests
import json

URL = 'http://localhost:8080/fetch_twitter'

def json_request(**params):
    response = requests.get(URL, params=params)
    return json.loads(response.content)


def main():
    handles = ['david_ziegler', 'ua6oxa', '_danilo', 'KeyserSosa']
    results = []
    data = json_request(handles=handles)
    while len(results) < len(handles):
        data = json_request(key=data['next_key'])
        print 'got result:', data['result']
        results.append(data['result'])

if __name__ == '__main__':
    main()
