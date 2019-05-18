import requests


def get_dog_image():
    r = requests.get("https://dog.ceo/api/breeds/image/random")
    return r.json().get("message")
