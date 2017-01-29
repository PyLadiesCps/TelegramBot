import json
import requests
import time
import urllib
import random
#import config

# edite aqui com seu token
TOKEN = "<your-bot-token>"


#TOKEN = config.token
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

imagens = list(range(6))

imagens[0] = "http://cdn3-www.cattime.com/assets/uploads/2011/08/best-kitten-names-1.jpg"
imagens[1] = "http://www.pets4homes.co.uk/images/articles/1646/large/kitten-emergencies-signs-to-look-out-for-537479947ec1c.jpg"
imagens[2] = "http://dreamatico.com/data_images/kitten/kitten-1.jpg"
imagens[3] = "https://pbs.twimg.com/profile_images/562466745340817408/_nIu8KHX.jpeg"
imagens[4] = "http://dreamatico.com/data_images/kitten/kitten-3.jpg"
imagens[5] = "https://upload.wikimedia.org/wikipedia/commons/thumb/0/06/Kitten_in_Rizal_Park,_Manila.jpg/230px-Kitten_in_Rizal_Park,_Manila.jpg"

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def echo_all(updates):
    for update in updates["result"]:
        text = update["message"]["text"]
        chat = update["message"]["chat"]["id"]
        send_message(text, chat)


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)

def send_kittens(updates):
	for update in updates["result"]:
		text = imagens[random.randint(0,5)]
		chat = update["message"]["chat"]["id"]
		send_message(text, chat)

def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            #echo_all(updates)
            send_kittens(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()