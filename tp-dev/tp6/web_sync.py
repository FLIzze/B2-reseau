import requests
import sys 

def main():
    arg = check_argument()
    html_content = get_content(arg)
    write_content(html_content, "/tmp/web_page.log")

def check_argument() -> str: 
    if len(sys.argv) == 1:
        print("missing an argument")
        exit(2)
    elif len(sys.argv) > 2:
        print("only one argument")
        exit(2)

    arg = sys.argv[1]
    return arg

def get_content(url: str) -> str: 
    try:
        html_content = requests.get(url)
    except:
        print("cant retrieve url")
        exit(3)
    print(html_content.text)
    if html_content.status_code != 200:
        print("bad status code")
        exit(3)
    return html_content.text

def write_content(content: str, file: str):
    with open(file, 'w') as web_page:
        web_page.write(content)
    web_page.close()

if __name__ == "__main__":
    main()
