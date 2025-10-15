from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
import random
import datetime
import requests
import pickle
import gc
import os


TELEGRAM_BOT_TOKEN = ""
CHAT_ID = ""

driver = webdriver.Chrome()

months_dictionary = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5,
                     "June": 6, "July": 7, "August": 8, "September": 9, "October": 10,
                     "November": 11, "December": 12}

MAX_RETRIES = 85

USERNAME = ""
PASSWORD = ""


def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.get(url, params=payload)

print(datetime.datetime.now())


def login():
    driver.get("https://ais.usvisa-info.com/en-ae/niv/users/sign_in")
    driver.maximize_window()

    time.sleep(3)
    body = driver.find_element(By.TAG_NAME, "body")
    for _ in range(1):
        body.send_keys(Keys.PAGE_DOWN)

    time.sleep(3)

    username = driver.find_element(By.XPATH, "/html/body/div[5]/main/div[3]/div/div[1]/div/form/div[1]/input")
    password = driver.find_element(By.XPATH, "/html/body/div[5]/main/div[3]/div/div[1]/div/form/div[2]/input")
    checkbox = driver.find_element(By.XPATH, "/html/body/div[5]/main/div[3]/div/div[1]/div/form/div[3]/label/div")

    username.send_keys(USERNAME)
    time.sleep(1)
    password.send_keys(PASSWORD)
    time.sleep(1)
    checkbox.click()
    time.sleep(1)
    password.send_keys(Keys.RETURN)
    time.sleep(8)
    #pickle.dump(driver.get_cookies(), open("coockies.pkl", "wb"))



def continue_to_calendar():
    time.sleep(random.randint(1, 5))
    for attempt in range(MAX_RETRIES):
        try:
            time.sleep(random.randint(1,7))
            continue_button = WebDriverWait(driver, 7).until(EC.visibility_of_element_located(
                (By.XPATH, "/html/body/div[4]/main/div[2]/div[2]/div[1]/div/div/div[1]/div[2]/ul/li")))
            continue_button.click()
            time.sleep(1)
            break
        except:
            print(f"Attempt {attempt + 1}: Continue field did not appear, refreshing...")
            driver.refresh()
            time.sleep(5)


    for attempt in range(MAX_RETRIES):
        try:
            first_reschedule_button = WebDriverWait(driver, 7).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "/html/body/div[4]/main/div[2]/div[2]/div/section/ul/li[3]/a/h5")))
            first_reschedule_button.click()
            time.sleep(0.5)
            break
        except:
            print(f"Attempt {attempt + 1}: 1st Schedule button field did not appear, refreshing...")
            driver.refresh()
            time.sleep(5)


    for attempt in range(MAX_RETRIES):
        try:
            second_reschedule_button = WebDriverWait(driver, 7).until(EC.visibility_of_element_located(
                (By.XPATH, "/html/body/div[4]/main/div[2]/div[2]/div/section/ul/li[3]/div/div/div[2]/p[2]/a")))
            second_reschedule_button.click()
            time.sleep(1)
            break
        except:
            print(f"Attempt {attempt + 1}: 2nd Schedule button field did not appear, refreshing...")
            driver.refresh()
            time.sleep(5)




def reschedule():
    available_dates = None
    earlier_date_found = False

    current_date = driver.find_element(By.XPATH, "/html/body/div[4]/main/div[2]/div[2]/div[1]/div/div/div[2]/p[1]").text.split(",")[
        0].split(" ")
    current_day = int(current_date[2])
    current_month = months_dictionary[current_date[3]]
    print("Current Scheduled Date: 2025", current_month, current_day, "\n")

    for j in range(1, 400):
        if j % 5 == 0:
            time.sleep(random.randint(7, 13))


        else:
            if earlier_date_found:
                break
            else:
                continue_to_calendar()

                for attempt in range(MAX_RETRIES):
                    try:
                        calendar_button = WebDriverWait(driver, 8).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[4]/main/div[4]/div/div/form/fieldset/ol/fieldset/div/div[2]/div[3]/li[1]/input")))
                        calendar_button.click()
                        time.sleep(0.5)
                        break

                    except:
                        print(f"Attempt {attempt + 1}: Calendar field did not appear, refreshing...")
                        driver.refresh()
                        time.sleep(5)

                for _ in range(1, 7):
                    available_dates = driver.find_elements(By.XPATH, "//a[@class='ui-state-default' and @href='#']")
                    if available_dates:
                        earliest_date = available_dates[0]
                        earliest_date.click()
                        time.sleep(0.5)

                        chosen_date = driver.find_element(By.XPATH,
                                                          "/html/body/div[4]/main/div[4]/div/div/form/fieldset/ol/fieldset/div/div[2]/div[3]/li[1]/input").get_attribute(
                            "value").split('-')
                        print("First Available Date:", chosen_date)

                        time_field = driver.find_element(By.ID, "appointments_consulate_appointment_time")
                        try:
                            if WebDriverWait(driver, 8).until(lambda driver: driver.find_element(By.XPATH, "/html/body/div[4]/main/div[4]/div/div/form/fieldset/ol/fieldset/div/div[2]/div[3]/li[2]/select/option[2]").get_attribute("value") != ""):
                                first_time_slot = driver.find_element(By.XPATH, "/html/body/div[4]/main/div[4]/div/div/form/fieldset/ol/fieldset/div/div[2]/div[3]/li[2]/select/option[2]").get_attribute("value")
                        except:
                            print("Time_slot failed, trying to close and start over.")
                            close_button = driver.find_element(By.XPATH, "/html/body/div[4]/main/div[4]/div/div/form/div[2]/fieldset/ol/a")
                            close_button.click()
                            break


                        print("First available time slot: ", first_time_slot, "\n")
                        time_dropdown = Select(time_field)
                        time_dropdown.select_by_value(first_time_slot)

                        new_month, new_day = int(chosen_date[1]), int(chosen_date[2])
                        if 4 < new_month < 8:                                                                           #current_month) or (new_month == current_month and new_day < current_day):
                            print(datetime.datetime.now(), "  Found an earlier date before August.\n")
                            #send_telegram_message(f"🚨FOUND A NEW DATE🚨 Day :{new_day}, Month: {new_month}")
                            #send_telegram_message("Finally.")

                            final_reschedule_button = driver.find_element(By.XPATH, "/html/body/div[4]/main/div[4]/div/div/form/div[2]/fieldset/ol/li/input")
                            final_reschedule_button.click()

                            confirm_button = WebDriverWait(driver, 300).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[7]/div/div/a[2]")))
                            confirm_button.click()

                            send_telegram_message("🚨 RESCHEDULED TO THAT DATE")

                            time.sleep(500)
                            print("Rescheduled to an earlier date. Closing the browser now... ")
                            earlier_date_found = True
                            break
                        else:
                            time.sleep(random.randint(1, 4))
                            close_button = driver.find_element(By.XPATH,
                                                               "/html/body/div[4]/main/div[4]/div/div/form/div[2]/fieldset/ol/a")
                            close_button.click()
                            time.sleep(random.randint(1, 3))
                            available_dates = None
                            gc.collect()
                            break

                    else:
                        #print("No available dates.")
                        next_button = driver.find_element(By.XPATH, "/html/body/div[5]/div[2]/div/a/span")
                        next_button.click()
                        time.sleep(0.5)




# try:
#     driver.get("https://ais.usvisa-info.com/en-ae/niv/groups/46635720")
#     cookies = pickle.load(open("cookies.pkl", "rb"))
#     for cookie in cookies:
#         driver.add_cookie(cookie)
#     driver.refresh()  # Apply cookies
#     driver.maximize_window()
#
#     print("✅ Loaded session. No need to log in again.")
# except:
#     print("⚠️ No saved cookies. Manual login required.")
#     driver.get("https://ais.usvisa-info.com/en-ae/niv/users/sign_in")
#     driver.maximize_window()
#     login()



login()

reschedule()
# time.sleep(180)
# reschedule()
send_telegram_message(f"Code execution finished. {datetime.datetime.now()}")
# for i in range(1, 2):
#     reschedule()
#     time.sleep(random.randint(500, 700))
#     print(f"Round {i} Finished\n")
#     print(datetime.datetime.now())

time.sleep(30)
print("\n")
print(datetime.datetime.now())
driver.close()
driver.quit()
#os.system("shutdown /s /t 20")


# # Function to check for available slots
#
#
# # Main loop to check periodically
# # try:
# #     login()
# #     while True:
# #         check_slots()
# #         time.sleep(600)  # Check every 10 minutes
# # except KeyboardInterrupt:
# #     print("Script stopped by user.")
# # finally:
# #     driver.quit()
#


# CALENDAR
# table_row = 1
# table_day = 1
#
# for _ in range(1, 7):
#     for _ in range(1, 6):
#         for _ in range(1, 8):
#             day = driver.find_element(By.XPATH, f"/html/body/div[5]/div[2]/table/tbody/tr[{table_row}]/td[{table_day}]").text
#             print(day)
#             table_day += 1
#
#         table_day = 1
#         table_row += 1
#     table_row = 1
#
#     next_button = driver.find_element(By.XPATH, "/html/body/div[5]/div[2]/div/a/span")
#     next_button.click()
#     time.sleep(2)

