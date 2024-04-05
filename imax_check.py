from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
import time
from datetime import date, timedelta

from send_email import send_email


def dune_url_with_date(date_str:str)->str:
    return f'https://www.amctheatres.com/movies/dune-part-two-68123/showtimes/dune-part-two-68123/{date_str}/amc-lincoln-square-13/all'


service = Service(executable_path='chromedriver-mac-x64/chromedriver')
driver = webdriver.Chrome(service=service)



try:
    
    latest_date = None
    none_found = 0
    
    for index in range(15):
        current_date = date.today() + timedelta(days=index)
        url = dune_url_with_date(str(current_date))
        time.sleep(1)
        driver.get(url)

        # Grab known element before checking whether optional element exists
        date_filter = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'showtimes-date-filter'))
        )
        

        no_showtimes = driver.find_elements(By.CLASS_NAME, 'Showtimes-unavailable-text')
        if no_showtimes:
            print(f'No Showtimes on {str(current_date)}')
            none_found += 1
            if none_found > 3:
                break
            
            continue

        theater = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'Theatre-Wrapper-First'))
        )

        showtime_formats = theater.find_element(By.CLASS_NAME, 'showtimes-format__h3')
        if showtime_formats.text == 'IMAX 70MM':
            latest_date = str(current_date)
            print(f'Imax available {str(current_date)}')
    

except Exception as e:
    print(e)

finally:
    
    with open('latest-date.txt','r+') as f:
        last_latest = f.read()
        if last_latest == '' or latest_date > last_latest:
            f.truncate()
            f.write(latest_date)
            send_email(f'Dates have been updated. Dune is now showing in Imax until {latest_date}')

        else:
            print('No updates')
    
    driver.quit()
    
