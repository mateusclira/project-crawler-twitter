import json
import os
import time
from tweepy import Stream
from decouple import config
from datetime import datetime
import argparse

consumer_key='SmkxOMAhcgKIFNlBjx0azHx0O'
consumer_secret='MO1GjsDEu9HuqP9MmZU55nXbhQcfFUcxMHyYsm3nleXHcsw1q7'
access_token='122195410-uEgiTnk85RJdB6QBhWv5QxcXZdWUgyFSALZcACh3'
access_token_secret ='XX6xgVi0sZEuZQmKlqy6z7zGuWRZvraFfAS4iYUUKxoD6'


# data_hoje = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
# out = open(f"collected_tweets_{data_hoje}.txt",'a')

import requests
import os
import json

# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ.get("AAAAAAAAAAAAAAAAAAAAALmiewEAAAAABF3XOa%2FDBz6CKr%2B3D5Y1WuwClSM%3DbZHRYWVEY9jh0ZB4kDXVe2nsOmWRUktuR2Efe2rGEQMczkDg3r")


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FilteredStreamPython"
    return r


def get_rules():
    response = requests.get(
        "https://api.twitter.com/1.1/tweets/search/stream/rules", auth=bearer_oauth
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))
    return response.json()


def delete_all_rules(rules):
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post(
        "https://api.twitter.com/1.1/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    print(json.dumps(response.json()))


def set_rules(delete):
    # You can adjust the rules if needed
    sample_rules = [
        {"tag": "bolsonaro"},
    ]
    payload = {"add": sample_rules}
    response = requests.post(
        "https://api.twitter.com/1.1/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload,
    )
    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))


def get_stream(set):
    response = requests.get(
        "https://api.twitter.com/1.1/tweets/search/stream", auth=bearer_oauth, stream=True,
    )
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            print(json.dumps(json_response, indent=4, sort_keys=True))


def main():
    rules = get_rules()
    delete = delete_all_rules(rules)
    set = set_rules(delete)
    get_stream(set)


if __name__ == "__main__":
    main()
    