import json

with open("urls.json", "r") as file:
    urls = json.load(file)['urls']
    for url in urls:
        print(url)

