from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.on("request", lambda request: print(">>", request.method, request.url))
    page.on("response", lambda response: print("<<", response.status, response.url))
    page.goto("https://jav.guru/308222/juq-377-happening-bar-married-woman-ntr-my-wife-who-once-said-its-for-your-sake-became-obsessed-with-cuckold-yuna-shiina/")
    page.get_by_role("link", name="STREAM ST").click()
    breakpoint()
    # page.frame_locator("iframe").locator("span").click()
    # page.frame_locator("iframe").locator("span").click()
    # page.frame_locator("iframe").locator("span").click()
    # page.frame_locator("iframe").locator("span").click()
    # page.frame(url="about:blank").get_by_text("Close").click()
    # page.frame(url="about:blank").locator("div").first.click()
    # page.frame(url="about:blank").get_by_text("Close").click()
    # page.frame(url="about:blank").locator("div").first.click()
    # page.frame_locator("iframe").frame_locator("iframe").locator("div:nth-child(41)").click()
    # page.frame_locator("iframe").locator("iframe").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
