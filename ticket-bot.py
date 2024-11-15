from constants import LINKS, PHONE

from playsound import playsound

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import mac_imessage

import time

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
        

def main():
    # create webdriver object
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)

    while True:
        for link in LINKS:
            try:
                driver.get(link)
                # closes pop up notification
                if check_element_exists_by_id(driver, "accept-and-continue-notification-text"):
                    button = driver.find_element(By.XPATH, "//button[@data-bdd='accept-modal-accept-button']")
                    button.click()
                # filters by 2 tickets
                ticket_count_filter = check_element_exists_by_id(driver, "filter-bar-quantity")
                if ticket_count_filter:
                    select = Select(ticket_count_filter)
                    select.select_by_value('2')

                # Checks that tickets are not sold out-takes 20 seconds to notify, but confirmed to work
                # if not (check_for_sold_out_notification(driver) or check_for_no_matching(driver)):
                #     print(f"TICKET FOUND FOR {link}")
                #     playsound('./sounds/found.wav')

                # Checks if tickets are available
                if check_element_exists_by_id(driver, "quickpicks-listings"):
                    ticket = driver.find_element(By.XPATH, "//*[@data-index='qp-0']")
                    ticket.click()
                    next_button = check_element_exists_by_xpath(driver, "//button[@data-bdd='offer-card-buy-button']")
                    if next_button:
                        next_button.click()
                        if check_element_exists_by_id(driver, "email[objectobject]__input"):
                            print(f"TICKET FOUND FOR {link}")
                            mac_imessage.send(f"FOUND TICKET: {link}", PHONE, 'iMessage')
                            playsound('./sounds/found.wav')
                            time.sleep(600)
            except Exception as e:
                print(e)
                playsound('./sounds/failure.wav')
            # finally:
            #     # Close the browser
            #     driver.quit()
        # time.sleep(30)

if __name__ == "__main__":
    main()