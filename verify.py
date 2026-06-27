from playwright.sync_api import sync_playwright

def run_cuj(page):
    page.goto("http://localhost:8000")
    page.wait_for_timeout(1000)

    # We want to fill out the form
    page.locator("#day-type").select_option("Busy workday")
    page.wait_for_timeout(500)
    page.locator("#diet").select_option("Vegetarian")
    page.wait_for_timeout(500)
    page.locator("#cuisine").select_option("Indian")
    page.wait_for_timeout(500)
    page.locator("#num-people").fill("2")
    page.wait_for_timeout(500)
    page.locator("#budget").fill("500")
    page.wait_for_timeout(500)
    page.locator("#ingredients-home").fill("rice, onions, tomatoes")
    page.wait_for_timeout(500)

    # Take screenshot of the form filled
    page.screenshot(path="/home/jules/verification/screenshots/verification.png")
    page.wait_for_timeout(1000)

if __name__ == "__main__":
    import os
    os.makedirs("/home/jules/verification/screenshots", exist_ok=True)
    os.makedirs("/home/jules/verification/videos", exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            record_video_dir="/home/jules/verification/videos"
        )
        page = context.new_page()
        try:
            run_cuj(page)
        finally:
            context.close()
            browser.close()
