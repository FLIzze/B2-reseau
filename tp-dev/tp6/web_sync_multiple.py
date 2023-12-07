import json
import requests
import time
import sys 

def main():
    arg = check_argument()
    html_content = get_content()
    write_content(html_content, "/tmp/web_page.log")

def check_argument():
    if len(sys.argv) != 1:
        print("no argument")
        exit(2)

def get_content() -> str: 
    with open("urls.json", "r") as file:
        urls = json.load(file)['urls']
        for url in urls:
            try:
                html_content = requests.get(url)
            except:
                print("cant retrieve url")
                exit(3)
            if html_content.status_code != 200:
                print("bad status code")
                exit(3)
    return html_content.text

def write_content(content: str, file: str):
    with open(file, 'w') as web_page:
        web_page.write(content + "\n\n\n\n\n")
    web_page.close()

if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    total_time = end - start
    print(f"time of execution: {total_time}s")
