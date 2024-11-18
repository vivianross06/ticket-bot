from constants import LINKS, PHONE, SIGN_IN, EMAIL, PASSWORD

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
    
def log_in(driver):
    # check if already logged in
    try:
        driver.get(SIGN_IN)
        email = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "email[objectobject]__input")))
    except TimeoutException:
        print("already logged in")
        return
    # logs in
    try:
        email.send_keys(EMAIL)
        password = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "password[objectobject]__input")))
        password.send_keys(PASSWORD)
        sign_in_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.NAME, "sign-in")))
        sign_in_button.click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@data-testid='accountLink']")))
    except Exception as e:
        print("error logging in")
        print(e)
        playsound('./sounds/failure.wav')
        raise e

def main():
    # create webdriver object
    options = webdriver.ChromeOptions()
    options.page_load_strategy = 'none'
    driver = webdriver.Chrome()
    driver.implicitly_wait(0)

    # logs in
    log_in(driver)

    time_start = datetime.now()


    while True:
        time_now = datetime.now()
        time_diff = time_now-time_start
        if time_diff.seconds > 1800:
            if find_present_explicit_wait_xpath(driver, "//button[@data-bdd='identity-login-login-button']", 5):
                print("reauntheticating")
                log_in(driver)
            else:
                print("already logged in, no need to reauthenticate")
            time_start = datetime.now()
        for link in LINKS:
            try:
                driver.get(link)
                # closes pop up notification
                button = find_clickable_explicit_wait_xpath(driver, "//button[@data-bdd='accept-modal-accept-button']", 5)
                if button:
                    button.click()
                # filters by 2 tickets
                ticket_count_filter = find_clickable_explicit_wait_id(driver, "filter-bar-quantity", 5)
                if ticket_count_filter:
                    select = Select(ticket_count_filter)
                    select.select_by_value('2')

                # Checks if tickets are available
                ticket = find_clickable_explicit_wait_xpath(driver, "//*[@data-index='qp-0']", 5)
                if ticket:
                    ticket.click()
                    next_button = find_clickable_explicit_wait_xpath(driver, "//button[@data-bdd='offer-card-buy-button']", 5)
                    if next_button:
                        next_button.click()
                        if find_present_explicit_wait_xpath(driver, "//h1[@class='style__Title-sc-10x7mpm-21 kKixwu']", 10):
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