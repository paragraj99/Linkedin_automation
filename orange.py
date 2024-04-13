# from selenium.webdriver.common.by import By
# from selenium import webdriver
# import time
# import pandas as pd
# from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
# # from selenium.common.exceptions import NoSuchElementException
# # from selenium.common.exceptions import ElementClickInterceptedException
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.options import Options

# # Specify the debugging address for the already opened Chrome browser
# debugger_address = 'localhost:8989'
# # Set up ChromeOptions and connect to the existing browser
# c_options = Options()
# c_options.add_experimental_option("debuggerAddress", debugger_address)
# # Initialize the WebDriver with the existing Chrome instance
# driver = webdriver.Chrome(options=c_options)

# # Initialize lists to store company information
# company_names = []
# employees = []
# profiles = []
# cities = []
# durations = []

# def scrape_employees():
#     try:
#         time.sleep(10)
#         scroll_down = driver.find_element(By.XPATH, '/html/body/main/div[1]/div[2]/div[2]')
#         scroll_down.click()

#         driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
#         time.sleep(20)

#         # Extract employees names, profiles, cities and duration of work from elements
#         company_name_elements = driver.find_elements(By.CSS_SELECTOR, '.artdeco-pill')

#         employee_names = driver.find_elements(By.CSS_SELECTOR, '.artdeco-entity-lockup__title')

#         employee_profiles = driver.find_elements(By.CSS_SELECTOR, '.artdeco-entity-lockup__subtitle')

#         employee_cities = driver.find_elements(By.CSS_SELECTOR, '.artdeco-entity-lockup__caption')

#         employee_durations = driver.find_elements(By.CSS_SELECTOR, '.artdeco-entity-lockup__metadata')

#         company_name = None

#         if not company_name_elements:
#             company_name = "Not found"
#         else:
#             company_name = company_name_elements[0].text.strip()
        
#         print('\ncompany : ', company_name)
#         company_names.extend([company_name] * len(employee_names))

#         for index, (name, profile, city, duration) in enumerate(zip(employee_names, employee_profiles, employee_cities, employee_durations)):
#             employee_name, employee_profile, employee_city, employee_duration = map(lambda x: x.text.strip(), (name, profile, city, duration))
            
#             print(f"Employee {index + 1}: Name: {employee_name}, Profile: {employee_profile}, City: {employee_city}, Duration: {employee_duration}")
            
#             employees.append(employee_name)
#             profiles.append(employee_profile)
#             cities.append(employee_city)
#             durations.append(employee_duration)

#         time.sleep(30)
    
#     except Exception as e:
#         print(f"error occurred in scroll down: {e}")



# def export_employee_info():

#     global company_names, employees, profiles, cities, durations

#     # Truncate lists to match the length of the shortest list
#     min_length = min(len(company_names), len(employees), len(profiles), len(cities), len(durations))
    
#     company_names = company_names[:min_length]
#     employees = employees[:min_length]
#     profiles = profiles[:min_length]
#     cities = cities[:min_length]
#     durations = durations[:min_length]

#     # Create a DataFrame from the collected data
#     df = pd.DataFrame({
#         'Company Names': company_names,
#         'Employee Names': employees,
#         'Employee Profiles': profiles,
#         'Employee cities': cities,
#         'Employee Durations': durations,
#     })

#     # Check if data was successfully collected and DataFrame was created
#     if not df.empty:
#         df.to_excel('linkedin_employee_info.xlsx', index=False)
#         print("\nData successfully exported to 'linkedin_employee_info.xlsx'")
#     else:
#         print("No data found to export")



# def scrape_linkedin_data(my_list):
    
#     page_count = 1

#     for url in my_list:
#         try:
#             add_url = url + 'people/' # Direct open people option 
#             driver.get(add_url)
#             time.sleep(30)

#             decision_makers = driver.find_element(By.CSS_SELECTOR, '.org-people-decision-makers-upsell-card__link-text')
#             decision_makers.click()
#             time.sleep(10)

#             # Switch to the new tab 
#             p = driver.current_window_handle
#             parent = driver.window_handles[0]
#             chld = driver.window_handles[1]
#             driver.switch_to.window(chld)
#             time.sleep(5)

#             print('\nTrying to scrap the Comapny data')

#             scrape_employees()

#             while True:
#                 next_page = driver.find_element(By.XPATH, '/html/body/main/div[1]/div[2]/div[2]/div[2]/div[5]/div/button[2]/span')

#                 try:
#                     print('\nPage No:', page_count, 'data scraped')
#                     next_page.click()
#                     time.sleep(10)
#                     scrape_employees()
#                     page_count += 1

#                 except ElementClickInterceptedException:
#                     print("\nNo more pages to scrap")
#                     print('\nTotal pages scraped:', page_count)
#                     # Close browser tab window
#                     driver.close()
#                     time.sleep(5)
                
#                 except NoSuchElementException:
#                     print("\nNo more pages to scrap parag")
#                     print('\nTotal pages scraped parag:', page_count)
#                     # Close browser tab window
#                     driver.close()
#                     time.sleep(5)

#         except Exception as e:
#             print(f"\nerror occurred : {e}")

#         driver.close()
#         driver.switch_to.window(p)

#     # Now start data to export into the excel
#     export_employee_info()

# # my_list = ['https://www.linkedin.com/company/vanlanschotkempeninvestmentbanking/', 'https://www.linkedin.com/company/js-bank/']
# # my_list = ['https://www.linkedin.com/company/js-bank/']
# # my_list = ['https://www.linkedin.com/company/vanlanschotkempeninvestmentbanking/','https://www.linkedin.com/company/natixis-in-portugal/','https://www.linkedin.com/company/bankmuscat/','https://www.linkedin.com/company/arab-national-bank/']
# my_list = ['https://www.linkedin.com/company/natixis-in-portugal/','https://www.linkedin.com/company/bankmuscat/','https://www.linkedin.com/company/arab-national-bank/']

# scrape_linkedin_data(my_list)
















































from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import pandas as pd
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
# from selenium.common.exceptions import NoSuchElementException
# from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# Specify the debugging address for the already opened Chrome browser
debugger_address = 'localhost:8989'
# Set up ChromeOptions and connect to the existing browser
c_options = Options()
c_options.add_experimental_option("debuggerAddress", debugger_address)
# Initialize the WebDriver with the existing Chrome instance
driver = webdriver.Chrome(options=c_options)

# Initialize lists to store company information
company_names = []
employees = []
profiles = []
cities = []
durations = []

def scrape_employees():
    try:
        time.sleep(3)
        scroll_down = driver.find_element(By.XPATH, '/html/body/main/div[1]/div[2]/div[2]')
        scroll_down.click()

        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(5)

        # Extract employees names, profiles, cities and duration of work from elements
        company_name_elements = driver.find_elements(By.CSS_SELECTOR, '.artdeco-pill')

        employee_names = driver.find_elements(By.CSS_SELECTOR, '.artdeco-entity-lockup__title')

        employee_profiles = driver.find_elements(By.CSS_SELECTOR, '.artdeco-entity-lockup__subtitle')

        employee_cities = driver.find_elements(By.CSS_SELECTOR, '.artdeco-entity-lockup__caption')

        employee_durations = driver.find_elements(By.CSS_SELECTOR, '.artdeco-entity-lockup__metadata')

        company_name = None

        if not company_name_elements:
            company_name = "Not found"
        else:
            company_name = company_name_elements[0].text.strip()
        
        print('\ncompany : ', company_name)
        company_names.extend([company_name] * len(employee_names))

        for index, (name, profile, city, duration) in enumerate(zip(employee_names, employee_profiles, employee_cities, employee_durations)):
            employee_name, employee_profile, employee_city, employee_duration = map(lambda x: x.text.strip(), (name, profile, city, duration))
            
            print(f"Employee {index + 1}: Name: {employee_name}, Profile: {employee_profile}, City: {employee_city}, Duration: {employee_duration}")
            
            employees.append(employee_name)
            profiles.append(employee_profile)
            cities.append(employee_city)
            durations.append(employee_duration)

        time.sleep(15)
    
    except Exception as e:
        print(f"error occurred in scroll down: {e}")



def export_employee_info():

    global company_names, employees, profiles, cities, durations

    # Truncate lists to match the length of the shortest list
    min_length = min(len(company_names), len(employees), len(profiles), len(cities), len(durations))
    
    company_names = company_names[:min_length]
    employees = employees[:min_length]
    profiles = profiles[:min_length]
    cities = cities[:min_length]
    durations = durations[:min_length]

    # Create a DataFrame from the collected data
    df = pd.DataFrame({
        'Company Names': company_names,
        'Employee Names': employees,
        'Employee Profiles': profiles,
        'Employee cities': cities,
        'Employee Durations': durations,
    })

    # Check if data was successfully collected and DataFrame was created
    if not df.empty:
        df.to_excel('linkedin_employee_info.xlsx', index=False)
        print("\nData successfully exported to 'linkedin_employee_info.xlsx'")
    else:
        print("No data found to export")



def scrape_linkedin_data(my_list):
    
    page_count = 1

    for url in my_list:
        try:
            add_url = url + 'people/' # Direct open people option 
            driver.get(add_url)
            time.sleep(5)

            decision_makers = driver.find_element(By.CSS_SELECTOR, '.org-people-decision-makers-upsell-card__link-text')
            decision_makers.click()
            time.sleep(5)

            # Switch to the new tab 
            p = driver.current_window_handle
            parent = driver.window_handles[0]
            chld = driver.window_handles[1]
            driver.switch_to.window(chld)
            time.sleep(5)

            print('\nTrying to scrap the Comapny data')

            scrape_employees()

            while True:
                next_page = driver.find_element(By.XPATH, '/html/body/main/div[1]/div[2]/div[2]/div[2]/div[5]/div/button[2]/span')

                print('\nPage No:', page_count, 'data scraped')
                next_page.click()
                time.sleep(10)
                
                scrape_employees()
                page_count += 1

        except Exception as e:
            print(f"\nerror occurred : {e}")

        driver.close()
        driver.switch_to.window(p)
        time.sleep(30)

    # Now start data to export into the excel
    export_employee_info()


# my_list = ['https://www.linkedin.com/company/js-bank/','https://www.linkedin.com/company/vanlanschotkempeninvestmentbanking/','https://www.linkedin.com/company/natixis-in-portugal/','https://www.linkedin.com/company/bankmuscat/','https://www.linkedin.com/company/arab-national-bank/']
my_list = input('Please enter the links with comma seprated: ')

scrape_linkedin_data(my_list)