from playwright.sync_api import Playwright, sync_playwright, expect
import galleryCrawler as gC
from pathlib import Path
from scrapy.http import HtmlResponse
from streamtape import main as st
from pyIDM import  download
from time import sleep
website = "jav.guru"
fp = r'D:\Developed\Automation\GalleryDownloader\galleryLinks.opml'

def alreadyNotDone(func):
    def wrapper(*args, **kwargs):
        filename = 'VideoList12'
        p = "".join(args[:-1])
        Path('list').parent.mkdir(exist_ok=True, parents=True)
        # Path("list").touch()
        ret = gC.rssImageExtractor()
        if ret.alreadyNotDownloaded(filename,p):
            try:
                func(*args, **kwargs)
            except:
                print('something wrong happened')
                return
            ret.downloadCompleteRegister(filename,p)
    return wrapper

def append_line_to_file(file_path, line_to_append):
    try:
        with open(file_path, 'a') as file:
            file.write(line_to_append + '\n')
        # print(f"Appended '{line_to_append}' to {file_path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def streamtapecall(rr):
    print(f'>>{rr.url=}')
    if "stre" in rr.url:
        breakpoint()


# @alreadyNotDone
def mainparse(url : str, browser):
    context = browser.new_context()
    page = context.new_page()
    page.on("request", lambda request: streamtapecall(request))
    page.on("response", lambda response: streamtapecall(response))
    page.goto(url)
    page.get_by_role("link", name="STREAM ST").click()
    # if1 = page.frame_locator("#post-325518 iframe").frame_locator("iframe")
    page.frame_locator("#post-325518 iframe").first.locator("div.inner").first.evaluate("start_player()")
    sleep(10)
    breakpoint()
    for i in range(1,100):
        try:
            page.frame_locator("#post-325518 iframe").frame_locator("iframe").get_by_role("button", name="Play").click()
        except Exception as e:
            print(e)
            sleep(2)
    # download(r'C:\Heaven\Haven\brothel\Sherawali', filename, url_t)

# https://lexica.art/prompt/ca7f2856-8f79-4aa8-85c0-45d3e1ef8939
# https://image.lexica.art/full_jpg/0509ff23-a646-4345-97b9-6a781fa6ed37

    context.close()

def run(playwright: Playwright) -> None:
    urlsfile = r'links.opml'
    browser = playwright.chromium.launch(headless=False)
    # url = "https://jpbabe.com/av/av.php?file=juq-369.mp4"
    with open(urlsfile,"r") as fp:
        for url in fp:
            if website in url:
                mainparse(url, browser)
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
