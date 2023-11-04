from playwright.sync_api import Playwright, sync_playwright, expect
import galleryCrawler as gC
from pathlib import Path
from scrapy.http import HtmlResponse
from streamtape import main as st
website = "sextb.net"
fp = r'D:\Developed\Automation\GalleryDownloader\galleryLinks.opml'

def alreadyNotDone(func):
    def wrapper(*args, **kwargs):
        filename = 'VideoList1'
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
    if "streamtape" in rr.url:
        breakpoint()

# @alreadyNotDone
def mainparse(url : str, browser):
    context = browser.new_context()
    page = context.new_page()
    page.on("request", lambda request: streamtapecall(request))
    page.on("response", lambda response: print("<<", response.status, response.url))
    page.goto(url)
    breakpoint()
    page.get_by_role("link", name="Close").click()
    page.get_by_role("button", name=" ST").click()
    page.frame_locator("#sextb-player iframe").get_by_text("PausePlay").click()
    # append_line_to_file(fp, url_streamtape)

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
