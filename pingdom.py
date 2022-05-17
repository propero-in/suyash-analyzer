from RPA.Browser.Selenium import Selenium
from time import sleep

browser = Selenium()

def ping_analysis(url : str):
    browser.open_available_browser("https://tools.pingdom.com/")
    browser.input_text("xpath://input[@id = 'urlInput']", url)
    sleep(2)
    browser.click_element("xpath:/html/body/app-root/main/app-home-hero/header/section/app-test-runner/div/div[2]/div[2]/app-select")
    sleep(0.5)
    browser.click_element("xpath:/html/body/app-root/main/app-home-hero/header/section/app-test-runner/div/div[2]/div[2]/app-select/div/div[1]")
    sleep(3)
    browser.click_element("xpath://input[@value = 'START TEST']")
    browser.wait_until_page_contains_element("xpath://div[@class='button-container']", 40)
    sleep(8)
    li = browser.get_webelements("xpath://div[@class='value']")
    grade = browser.get_text(li[0])
    page_size = browser.get_text(li[1])
    load_time = browser.get_text(li[2])
    page_req = browser.get_text(li[3])
    browser.close_browser()
    return [grade, page_size, load_time, page_req]