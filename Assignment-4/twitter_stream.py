import socket
import json

from tweepy import OAuthHandler, Stream, StreamListener

from configuration import API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET


def get_auth():
    auth = OAuthHandler(API_KEY, API_KEY_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return auth


def get_socket(host, port):

    return c_socket


def extract_twitter_text(message):
    if "extended_tweet" in message:
        text = message['extended_tweet']['full_text']
    else:
        text = message['text']
    text = str(text + "\n").encode('utf-8')
    return text


class TweetListener(StreamListener):

    def __init__(self, client_socket):
        self.client_socket = client_socket

    def on_data(self, data):
        try:
            msg = json.loads(data)
            text = extract_twitter_text(msg)
            print(f"Message: {text}")
            self.client_socket.send(text)

        except BaseException as e:
            print(f"Error on_data: {e}")

        return True

    def on_error(self, status):
        print(status)
        return True


def send_data(c_socket, keyword):
    print("Start sending data from Twitter to socket")
    auth = get_auth()
    twitter_stream = Stream(auth, TweetListener(c_socket))
    twitter_stream.filter(track=keyword, languages=["en"])


if __name__ == "__main__":
    host = "127.0.0.1"
    port = 5556
    keywords = ["covid"]
    
    s = socket.socket()
    s.bind((host, port))
    print("Socket is established")

    s.listen(4)
    print("Socket is listening")

    c_socket, addr = s.accept()
    print("Received request from: " + str(addr))

    send_data(c_socket, keyword=keywords)
