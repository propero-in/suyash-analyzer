from RPA.Browser.Selenium import Selenium
from . import PageSpeedInsights as ps
from . import pingdom as pd
from . import WordDoc
from time import time, sleep
from selenium.common.exceptions import StaleElementReferenceException
from RPA.Email.ImapSmtp import ImapSmtp as email
import os
import json
import requests

browser = Selenium()
cwd = os.getcwd()
def open_browser(url):
    browser.open_available_browser("https://gtmetrix.com/")
    browser.maximize_browser_window()
    browser.input_text('xpath://input[@name="url"]', url)
    sleep(2)
    browser.click_button("Test your site")
    browser.wait_until_page_contains_element('xpath://div[@class="report-performance clear"]', 120)

def Screenshot():
    browser.screenshot('xpath://div[@class="report-scores"]', cwd+"/output/Gtmetrix/screenshot_1.png")
    sleep(0.5)
    browser.screenshot('xpath://div[@class="report-page-details"]', cwd+"/output/Gtmetrix/screenshot_2.png")
    sleep(0.5)
    browser.close_browser()

def shopify_analyze_website(url : str):
    try:
        cwd = os.getcwd()
        browser.open_available_browser("https://analyze.speedboostr.com/")
        browser.wait_until_page_contains_element("id:analyze-url", 120)
        sleep(3)
        if browser.is_element_visible("xpath://button[text() = 'Accept']"):
            browser.click_button("Accept")
        sleep(1)
        while True:
            sleep(0.5)
            if browser.is_element_visible("id:analyze-url") == False:
                continue
            browser.input_text("id:analyze-url", url)
            sleep(1)
            browser.click_button("Analyze")
            sleep(2)
            if browser.is_element_visible("xpath://div[text()='Analyzing...']") == False:
                continue
            if browser.is_element_visible("xpath://div[text()='Analyzing...']") == True:
                break
        browser.wait_until_page_contains_element("xpath://td[text() = 'Oversized images']", 300)
        sleep(1)
        li = browser.find_elements("xpath://td[@class = 'td-score']")
        num = browser.get_text(li[8])
        if num == "0":
            browser.close_browser()
            return(0)
        else:
            href = []
            browser.click_element("xpath://td[text() = 'Oversized images']")
            sleep(2)
            items = browser.find_elements("xpath://a")
            for item in items:
                link = browser.get_element_attribute(item, attribute="href")
                href.append(link)
            li2 = href[13:]
            li3 = li2[::-1]
            req_li = li3[20:]
            req_li = req_li[::-1]
            count = 1
            if len(req_li) == 1:
                a = req_li[0]
                response = requests.get(a)
                if "png" in a:
                    f = open(cwd+"/output/oversized_images/image1.png", "wb")
                else:
                    f = open(cwd+"/output/oversized_images/image1.jpg", "wb")
                f.write(response.content)
                f.close()
            if len(req_li) > 1:
                for i in req_li:
                    i1 = i[::-1]
                    i2 = i1[13:]
                    req_url = i2[::-1]
                    #return(i)
                    response = requests.get(req_url)
                    if "png" in req_url:
                        file = open(cwd+"/output/oversized_images/image"+str(count)+".png", "wb")
                        file.write(response.content)
                        file.close()
                    if "jpg" in req_url:
                        file = open(cwd+"/output/oversized_images/image"+str(count)+".jpg", "wb")
                        file.write(response.content)
                        file.close()
                    if "jpeg" in req_url:
                        file = open(cwd+"/output/oversized_images/image"+str(count)+".jpeg", "wb")
                        file.write(response.content)
                        file.close()
                    count += 1
            browser.close_browser()
    except StaleElementReferenceException:
        shopify_analyze_website(url)
    return("1")

def send_mails(url, recipient_email):
    site = url[12:]
    name_li = site.split(".")
    name = name_li[0]
    with open(cwd+"/Analyzer/emails.json", "r") as f:
        data = json.load(f)
    sender_email = data["sender"]["mail"]
    sender_password = data["sender"]["password"]
    mail = email(smtp_server="smtp.gmail.com", smtp_port=587)
    mail.authorize(account = sender_email, password = sender_password)
    mail.send_message(
    sender = sender_email,
    recipients = recipient_email,
    subject = "Your Website Analysis Report.",
    body = "Please find your website's analysis report based on lab data below.",
    attachments = [cwd+"/output/"+name+".docx"]
)

def remove_files():
    p1 = os.getcwd()+"/output/Gtmetrix"
    p2 = os.getcwd()+"/output/oversized_images"
    p3 = os.getcwd()+"/output/Compressed_Images"
    p4 = os.getcwd()+"/output/Desktop"
    p5 = os.getcwd()+"/output/Mobile"
    if os.listdir(p1) != 0:
        for f in os.listdir(p1):
            os.remove(os.path.join(p1, f))
    if os.listdir(p2) != 0:
        for f in os.listdir(p2):
            os.remove(os.path.join(p2, f))
    if os.listdir(p3) != 0:
        for f in os.listdir(p3):
            os.remove(os.path.join(p3, f))
    if os.listdir(p4) != 0:
        for f in os.listdir(p4):
            os.remove(os.path.join(p4, f))
    if os.listdir(p5) != 0:
        for f in os.listdir(p5):
            os.remove(os.path.join(p5, f))
    else:
        pass

def driver(website, email_address):
    browser = Selenium()
    start_time = time()
    try:
        open_browser(website)
        Screenshot()
    except Exception as e:
        browser.capture_page_screenshot(cwd+"/error.png")
        raise e
    var = shopify_analyze_website(website)
    score_list = ps.get_score(website)
    res = pd.ping_analysis(website)
    if var == 0:
        end_time = time()
        bot_time = end_time - start_time
        time_taken = round(bot_time, 2)
        WordDoc.create_document_1(website, time_taken, score_list, res)
    else:
        end_time = time()
        bot_time = end_time - start_time
        time_taken = round(bot_time, 2)
        WordDoc.create_document_2(website, time_taken, score_list, res)
    remove_files()
    sleep(2)
    browser.close_all_browsers()
    send_mails(website, email_address)
    remove_files()