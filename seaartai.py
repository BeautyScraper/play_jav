import shutil
from playwright.sync_api import Playwright, sync_playwright, expect
import galleryCrawler as gC
from pathlib import Path
from scrapy.http import HtmlResponse
from streamtape import main as st
from pyIDM import  download
from time import sleep
from aria2cgeneric import ariaDownload
import re
from proxy_loader import load_proxy_from_json
import json


website = "seaart.ai"
fp = r'D:\Developed\Automation\GalleryDownloader\galleryLinks.opml'
ddir_path = r'D:\paradise\stuff\new\jav'


def alreadyNotDone(func):
    def wrapper(*args, **kwargs):
        filename = website
        p = "".join(args[:-1])
        Path('list').parent.mkdir(exist_ok=True, parents=True)
        # Path("list").touch()
        ret = gC.rssImageExtractor()
        if ret.alreadyNotDownloaded(filename,p):
            try:
                func(*args, **kwargs)
            except Exception as e:
                print(f'Exception: {e}')
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

def streamtapecall(rr, filename):
    print(f'>>{rr.url=}')
    if ".mp4?response-content-disposition" in rr.url:
        breakpoint()
        ariaDownload(rr.url,ddir_path,filename)
        # download(videoUrl=rr.url,videoPath=ddir_path,filename=filename,forceDownload=False) 
        pass


def has_reached_end_of_page(page):
    # Evaluate JavaScript in the browser context
    return page.evaluate("""
        (function() {
            // Current scroll position
            const scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
            // Total scrollable height
            const scrollHeight = document.documentElement.scrollHeight || document.body.scrollHeight;
            // Viewport height
            const clientHeight = document.documentElement.clientHeight || window.innerHeight;
            // Check if we've reached the bottom
            return scrollTop + clientHeight >= scrollHeight;
        })()
    """)

@alreadyNotDone
def mainparse(urlt : str, browser):
    # context = browser.new_context()
    context = browser
    page = context.new_page()
    # page.on("request", lambda request: streamtapecall(request,filename))
    # page.on("response", lambda response: streamtapecall(response,filename))
    page.goto(urlt)
    # # with open("cookies.json", "w") as f:
    # #     f.write(json.dumps(context.cookies()))

    page.locator("#overview").get_by_text("View More").click()
    # storage = context.storage_state(path="state.json")
    # breakpoint()
    sleep(5)
    # filename = url.strip('/').split('/')[-1]
    while not has_reached_end_of_page(page):
        for _ in range(3):
            sleep(2)
            page.locator("body").press("PageDown")
        resp = HtmlResponse(url=urlt, body=page.content(), encoding='utf-8')
        # breakpoint()
        rt = resp.css('img[src*=low]::attr(src)').getall() 
        for url in rt:
            dir = Path(r'C:\Heaven\Haven\brothel') / resp.css('.overflow-ellipsis::text').get()
            ariaDownload(url.replace('low','high'),str(dir), url.split('/')[-1],1)
            # download(r'C:\Heaven\Haven\brothel\Sherawali',, url.replace('low','high'))
        sleep(5)

    # breakpoint()

    # filename = resp.css(".video-title::text").get()[:230] + '.mp4'
    # upat = '.+response-content-disposition.+' 
    # # upat = '.+mp4.+' 
    # page.locator("#player").get_by_role("button").last.click()
    # sleep(1)
    # with page.expect_request(lambda request: re.match(upat,request.url)) as first:
    #     page.locator("#player").get_by_role("button").first.click()
    #     # breakpoint()   
    # request = first.value
    # ariaDownload(request.url,ddir_path,filename)
    # list(map(lambda x:x.close(), context.pages[1:]))
    # print(first.value)    
    # sleep(60)
    # page.get_by_label("Play").click()
    # download(r'C:\Heaven\Haven\brothel\Sherawali', filename, url_t)

# https://lexica.art/prompt/ca7f2856-8f79-4aa8-85c0-45d3e1ef8939
# https://image.lexica.art/full_jpg/0509ff23-a646-4345-97b9-6a781fa6ed37

    # context.close()

def run(playwright: Playwright) -> None:
    urlsfile = r'sealinks.opml'
    browser = playwright.chromium.launch(headless=False)
    user_data_dir = Path(r'C:\dumpinggrounds\playwright_data2')
    user_data_dir.mkdir(exist_ok=True,parents=True)
    shutil.rmtree(user_data_dir)
    user_data_dir.mkdir(exist_ok=True,parents=True)
    proxy = load_proxy_from_json('proxies.json')

    # url = "https://jpbabe.com/av/av.php?file=juq-369.mp4"
    # browser = playwright.chromium.launch_persistent_context(user_data_dir,headless=False,proxy=proxy)
    # browser = playwright.chromium.launch_persistent_context(user_data_dir,headless=False,args=["--disable-blink-features=AutomationControlled"])
    browser = browser.new_context(storage_state="state.json")
    with open(urlsfile,"r") as fp:
        for url in fp:
            if website in url:
                mainparse(url, browser)
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
