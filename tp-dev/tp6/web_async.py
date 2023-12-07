import sys 
import asyncio
import aiohttp
import aiofiles

async def main():
    arg = await check_argument()
    html_content = await get_content(arg)
    await write_content(html_content, "/tmp/web_page.log")

async def check_argument() -> str: 
    if len(sys.argv) == 1:
        print("missing an argument")
        exit(2)
    elif len(sys.argv) > 2:
        print("only one argument")
        exit(2)

    arg = sys.argv[1]
    return arg

async def get_content(url: str) -> str: 
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    print("bad status code")
                    exit(3)
                return await response.text()
    except:
        print("cant retrieve url")
        exit(3)

async def write_content(content: str, file: str):
    async with aiofiles.open(file, mode='w') as web_page:
        await web_page.write(content)
    web_page.close()

if __name__ == "__main__":
    asyncio.run(main())
