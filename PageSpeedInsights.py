from RPA.Browser.Selenium import Selenium
from time import sleep
from selenium.common.exceptions import ElementNotInteractableException
from SeleniumLibrary.errors import NoOpenBrowser
import os

browser = Selenium()
cwd = os.getcwd()
t_1 = ""
t_2 = ""
lcp_score = ""
flag = 0

def remove_files():
    p1 = cwd+"/output/Mobile"
    p2 = cwd+"/output/Desktop"
    if os.listdir(p1) != 0:
        for f in os.listdir(p1):
            os.remove(os.path.join(p1, f))
    if os.listdir(p2) != 0:
        for f in os.listdir(p2):
            os.remove(os.path.join(p2, f))
    else:
        pass

def get_score(url):
    global t_1
    global t_2
    global flag
    global lcp_score
    try:
        browser.open_available_browser("https://pagespeed.web.dev/")
        sleep(2)
        if browser.is_element_visible("xpath://span[text() = 'Ok, Got it.']") == True:
            browser.click_element("xpath://span[text() = 'Ok, Got it.']")
        sleep(1)
        while True:
            sleep(0.5)
            if browser.is_element_visible("xpath://input[@name = 'url']") == False:
                continue
            browser.input_text("xpath://input[@name = 'url']", url)
            sleep(1)
            browser.click_button("Analyze")
            sleep(2)
            if browser.is_element_visible("xpath://div[text()='Running performance analysis']") == False:
                continue
            if browser.is_element_visible("xpath://div[text()='Running performance analysis']") == True:
                break
        browser.wait_until_element_is_not_visible("xpath://div[text()='Running performance analysis']", 120)
        sleep(5)
        if browser.is_element_visible("xpath:div[text()='Oops! Something went wrong.']") == True:
            browser.close_all_browsers()
            sleep(0.5)
            get_score(url)
        if browser.is_element_visible("xpath://span[text() = 'First Contentful Paint']") == False:
            browser.close_all_browsers()
            sleep(0.5)
            get_score(url)
        sleep(10)
        if browser.is_element_visible("xpath://div[@class='lh-gauge__percentage']") == True:
            e = browser.get_webelements("xpath://div[@class='lh-gauge__percentage']")
        else:
            browser.close_all_browsers()
            sleep(0.5)
            get_score(url)
        if len(e) == 2:
            t_1 = browser.get_text(e[0])
        else:
            browser.close_all_browsers()
            sleep(0.5)
            get_score(url)
        if browser.is_element_visible("xpath://div[@class = 'lh-audit-group lh-audit-group--metrics']"):
            es = browser.get_webelements("xpath://div[@class = 'lh-audit-group lh-audit-group--metrics']")
            browser.screenshot(es[0], "output/Mobile/webvitals.png")
        else:
            browser.close_all_browsers()
            sleep(0.5)
            remove_files()
            get_score(url)
        if browser.is_element_visible("xpath://div[@class = 'lh-audit-group lh-audit-group--load-opportunities']"):
            es_2 = browser.get_webelements("xpath://div[@class = 'lh-audit-group lh-audit-group--load-opportunities']")
        else:
            browser.close_all_browsers()
            sleep(0.5)
            get_score(url)
        if len(es_2) == 0:
            flag = 1
        if flag == 0:
            if es_2[0].size["height"] != 0 and es_2[0].size["width"] != 0:
                browser.screenshot(es_2[0], "output/Mobile/opportunities.png")
        sleep(1)
        lcp = browser.get_webelements("xpath://div[@class='lh-metric__value']")
        lcp_score = browser.get_text(lcp[4])
        sleep(1)
        browser.click_button("//button[@id='desktop_tab']")
        sleep(5)
        browser.execute_javascript("window.scrollTo(0, 0);")
        t_2 = browser.get_text(e[1])
        sleep(2)
        browser.scroll_element_into_view(es[1])
        sleep(1)
        browser.screenshot(es[1], "output/Desktop/webvitals.png")
        sleep(2)
        if flag == 0 and len(es_2) == 2:
            if es_2[1].size["height"] != 0 and es_2[1].size["width"] != 0:
                browser.screenshot(es_2[1], "output/Desktop/opportunities.png")
        sleep(1)
        browser.close_all_browsers()
    except NoOpenBrowser or ElementNotInteractableException or AssertionError or IndexError:
        if IndexError:
            pass
        sleep(0.5)
        print("some error occured, reloading.")
        browser.close_all_browsers()
        remove_files()
        get_score(url)
    return [t_1, t_2, lcp_score]