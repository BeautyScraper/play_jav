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


website = "javtiful"
fp = r'D:\Developed\Automation\GalleryDownloader\galleryLinks.opml'
ddir_path = r'D:\paradise\stuff\new\jav'


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

def streamtapecall(rr, filename):
    print(f'>>{rr.url=}')
    if ".mp4?response-content-disposition" in rr.url:
        breakpoint()
        ariaDownload(rr.url,ddir_path,filename)
        # download(videoUrl=rr.url,videoPath=ddir_path,filename=filename,forceDownload=False) 
        pass


@alreadyNotDone
def mainparse(url : str, browser):
    # context = browser.new_context()
    context = browser
    page = context.new_page()
    # page.on("request", lambda request: streamtapecall(request,filename))
    # page.on("response", lambda response: streamtapecall(response,filename))
    page.goto(url)
    # breakpoint()
    filename = url.strip('/').split('/')[-1]
    resp = HtmlResponse(url=url, body=page.content(), encoding='utf-8')
    # breakpoint()
    filename = resp.css(".video-title::text").get()[:230] + '.mp4'
    upat = '.+response-content-disposition.+' 
    # upat = '.+mp4.+' 
    page.locator("#player").get_by_role("button").last.click()
    sleep(1)
    with page.expect_request(lambda request: re.match(upat,request.url)) as first:
        page.locator("#player").get_by_role("button").first.click()
        # breakpoint()   
    request = first.value
    ariaDownload(request.url,ddir_path,filename)
    list(map(lambda x:x.close(), context.pages[1:]))
    # print(first.value)    
    # sleep(30)
    # page.get_by_label("Play").click()
    # download(r'C:\Heaven\Haven\brothel\Sherawali', filename, url_t)

# https://lexica.art/prompt/ca7f2856-8f79-4aa8-85c0-45d3e1ef8939
# https://image.lexica.art/full_jpg/0509ff23-a646-4345-97b9-6a781fa6ed37

    # context.close()

def run(playwright: Playwright) -> None:
    urlsfile = r'links.opml'
    # browser = playwright.chromium.launch(headless=False)
    user_data_dir = Path(r'C:\dumpinggrounds\playwright_data')
    for _ in range(1,1000000):
        shutil.rmtree(user_data_dir)
        user_data_dir.mkdir(exist_ok=True,parents=True)
        proxy = load_proxy_from_json('proxies.json')

        browser = playwright.chromium.launch_persistent_context(user_data_dir,headless=False,proxy=proxy)
        context = browser
        page = context.new_page() 
        try:
            page.goto('https://mrdeepfakes.com/',timeout=600000,)
            print(proxy)
            breakpoint()
        except Exception as e:
            print(e)
        browser.close()
    # url = "https://jpbabe.com/av/av.php?file=juq-369.mp4"
    with open(urlsfile,"r") as fp:
        for url in fp:
            if website in url:
                mainparse(url, browser)

with sync_playwright() as playwright:
    run(playwright)
