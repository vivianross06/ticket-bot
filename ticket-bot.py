from constants import LINKS, PHONE

from playsound import playsound

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import mac_imessage

import time
from datetime import datetime

def check_element_exists_by_id(driver, element):
    try:
        ele = driver.find_element(By.ID, element)
        return ele
    except NoSuchElementException:
        return None

def check_element_exists_by_xpath(driver, element):
    try:
        ele = driver.find_element(By.XPATH, element)
        return ele
    except NoSuchElementException:
        return None

def check_for_sold_out_notification(driver):
    try:
        driver.find_element(By.XPATH, "//div[@data-bdd='canceled-event-header-title']")
        return True
    except NoSuchElementException:
        return False

def check_for_no_matching(driver):
    try:
        driver.find_element(By.ID, "noMatching")
        return True
    except NoSuchElementException: 
        return False
    
def find_clickable_explicit_wait_xpath(driver, xpath, duration):
    try:
        button = WebDriverWait(driver, duration).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        return button
    except TimeoutException:
        return None

def find_clickable_explicit_wait_id(driver, id, duration):
    try:
        button = WebDriverWait(driver, duration).until(EC.element_to_be_clickable((By.ID, id)))
        return button
    except TimeoutException:
        return None

def find_present_explicit_wait_id(driver, id, duration):
    try:
        element = WebDriverWait(driver, duration).until(EC.presence_of_element_located((By.ID, id)))
        return element
    except TimeoutException:
        return None
    
def find_present_explicit_wait_xpath(driver, xpath, duration):
    try:
        element = WebDriverWait(driver, duration).until(EC.presence_of_element_located((By.XPATH, xpath)))
        return element
    except TimeoutException:
        return None
        

def main():
    # create webdriver object
    options = webdriver.ChromeOptions()
    options.page_load_strategy = 'none'
    driver = webdriver.Chrome()
    driver.implicitly_wait(0)

    while True:
        for link in LINKS:
            try:
                driver.get(link)
                # closes pop up notification
                # button = check_element_exists_by_xpath(driver, "//button[@data-bdd='accept-modal-accept-button']")
                button = find_clickable_explicit_wait_xpath(driver, "//button[@data-bdd='accept-modal-accept-button']", 5)
                # button = find_clickable_explicit_wait_xpath(driver, "/html/body/div[2]/div/div[7]/div/div/div[3]/div/button", 5)
                if button:
                    button.click()
                # filters by 2 tickets
                # ticket_count_filter = check_element_exists_by_id(driver, "filter-bar-quantity")
                ticket_count_filter = find_clickable_explicit_wait_id(driver, "filter-bar-quantity", 5)
                if ticket_count_filter:
                    select = Select(ticket_count_filter)
                    select.select_by_value('2')

                # Checks that tickets are not sold out-takes 20 seconds to notify, but confirmed to work
                # if not (check_for_sold_out_notification(driver) or check_for_no_matching(driver)):
                #     print(f"TICKET FOUND FOR {link}")
                #     playsound('./sounds/found.wav')

                # Checks if tickets are available
                # ticket = check_element_exists_by_xpath(driver, "//*[@data-index='qp-0']")
                ticket = find_clickable_explicit_wait_xpath(driver, "//*[@data-index='qp-0']", 5)
                if ticket:
                    ticket.click()
                    # next_button = check_element_exists_by_xpath(driver, "//button[@data-bdd='offer-card-buy-button']")
                    next_button = find_clickable_explicit_wait_xpath(driver, "//button[@data-bdd='offer-card-buy-button']", 5)
                    if next_button:
                        next_button.click()
                        # driver.implicitly_wait(10)
                        # if check_element_exists_by_id(driver, "email[objectobject]__input"):
                        if find_present_explicit_wait_id(driver, "email[objectobject]__input", 5):
                            # driver.implicitly_wait(6)
                            print(f"{datetime.now()} TICKET FOUND FOR {link}")
                            # mac_imessage.send(f"FOUND TICKET: {link}", PHONE, 'iMessage')
                            playsound('./sounds/found.wav')
                            time.sleep(600)
                        else:
                            print(f"{datetime.now()} Tickets were available for {link}. But they're gone now :(")
            except Exception as e:
                print(e)
                playsound('./sounds/failure.wav')
                time.sleep(600)
            # finally:
            #     # Close the browser
            #     driver.quit()
        # time.sleep(30)

if __name__ == "__main__":
    main()