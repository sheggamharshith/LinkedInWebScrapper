import csv
from parsel import Selector
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

def linkedIn_Scrapping(domain,area,email,password):
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

    creds = ServiceAccountCredentials.from_json_keyfile_name("LinkedInScrapping-e0f14006296b.json", scope)

    client = gspread.authorize(creds)

    sheet = client.open("LinkedInData").sheet1  # Open the spreadhseet

    sheet.insert_row(['name', 'job_title', 'schools', 'location', 'ln_url'])

    driver = webdriver.Chrome('/Users/harshithsheggam/Downloads/chromedriver')

    driver.get('https://www.linkedin.com/')

    driver.find_element_by_xpath('//a[text()="Sign in"]').click()

    username_input = driver.find_element_by_name('session_key')
    username_input.send_keys(email)

    password_input = driver.find_element_by_name('session_password')
    password_input.send_keys(password)

    # click on the sign in button
    # we're finding Sign in text button as it seems this element is seldom to be changed
    driver.find_element_by_xpath('//button[text()="Sign in"]').click()

    driver.get('https://www.google.com/')

    search_input = driver.find_element_by_name('q')
    # let google find any linkedin user with keyword "python developer" and "San Francisco"
    search_input.send_keys('site:linkedin.com/in/ AND {} AND {}'.format(domain,area))

    search_input.send_keys(Keys.RETURN)

    # grab all linkedin profiles from first page at Google
    profiles = driver.find_elements_by_xpath('//*[@class="r"]/a[1]')
    profiles = [profile.get_attribute('href') for profile in profiles]

    # visit each profile in linkedin and grab detail we want to get
    for profile in profiles:
        driver.get(profile)

        try:
            sel = Selector(text=driver.page_source)
            name = sel.xpath('//title/text()').extract_first().split(' | ')[0]
            job_title = sel.xpath('//h2/text()').extract_first()
            schools = ', '.join(sel.xpath('//*[contains(@class, "pv-entity__school-name")]/text()').extract())
            location = sel.xpath('//*[@class="t-16 t-black t-normal inline-block"]/text()').extract_first()
            ln_url = driver.current_url
            """
            you can add another logic in case parsing is failed, ie because no job title is found
            because the linkedin user isn't add it
            """
        except Exception as e:
            print('failed')
            print(e)

        # print to console for testing purpose
        print('\n')
        print(name)
        print(job_title)
        print(schools)
        print(location)
        print(ln_url)
        print('\n')

        sheet.insert_row([name, job_title, schools, location, ln_url])

    driver.quit()

