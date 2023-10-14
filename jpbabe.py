from playwright.sync_api import Playwright, sync_playwright, expect
import galleryCrawler as gC
from pathlib import Path

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

@alreadyNotDone
def mainparse(url : str, browser):
    context = browser.new_context()
    page = context.new_page()
    page.goto(url)
    # breakpoint()
    urlu = page.locator("p:nth-child(3) > a").get_attribute('href')
    page.goto(urlu)
    page.get_by_role("button", name="GET THE VIDEO LINK - CLICK HERE").click()
    # breakpoint()
    url_streamtape = page.locator('css=a[href*=stream]').last.get_attribute('href')
    append_line_to_file(fp, url_streamtape)

    context.close()

def run(playwright: Playwright) -> None:
    urlsfile = r'links.opml'
    browser = playwright.chromium.launch(headless=False)
    # url = "https://jpbabe.com/av/av.php?file=juq-369.mp4"
    with open(urlsfile,"r") as fp:
        for url in fp:
            mainparse(url, browser)
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
