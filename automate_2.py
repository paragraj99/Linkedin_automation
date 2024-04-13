from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import pandas as pd
from selenium.webdriver.chrome.options import Options

# Specify the debugging address for the already opened Chrome browser
debugger_address = 'localhost:8989'

# Set up ChromeOptions and connect to the existing browser
c_options = Options()
c_options.add_experimental_option("debuggerAddress", debugger_address)

# Initialize the WebDriver with the existing Chrome instance
driver = webdriver.Chrome(options=c_options)

try:
    # my_list = ['https://www.linkedin.com/showcase/deloitte-corporate-finance/','https://www.linkedin.com/company/responza/','https://www.linkedin.com/company/evaitcs/']
    # my_list = ['https://www.linkedin.com/company/evaitcs/','https://www.linkedin.com/company/responza/','https://www.linkedin.com/company/insight-global-it-services-solution/']
    my_list = input("Enter links with comma seprated links : ").split(",")

    # Initialize lists to store company information
    company_names = []
    employees = []
    profiles = []

    for url in my_list:
        add_url = url + 'people/' # Direct open people option 

        driver.get(add_url)

        # Scroll down to the bottom of the page to load more content
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(10)  # Adjust the sleep time as needed
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            time.sleep(5)

        # Extract company_name, employee_name, profile from elements
        company_name_element = driver.find_elements(By.CSS_SELECTOR, '.organization-outlet .org-top-card-summary__title')

        employee_names = driver.find_elements(By.CSS_SELECTOR, '.org-people-profile-card__profile-title.org-people-profile-card__profile-title')

        employee_profiles = driver.find_elements(By.CSS_SELECTOR, '.artdeco-entity-lockup--size-7 .artdeco-entity-lockup__subtitle')

        company_name = None

        for index, company in enumerate(company_name_element):
            if index == 0:
                company_name = company.text.strip()
                company_names.extend([company_name] * len(employee_names))
            else:
                company_names.append(company_name)

        for name in employee_names:
            employee_name = name.text.strip()
            employees.append(employee_name)

        for profile in employee_profiles:
            employee_profile = profile.text.strip()
            profiles.append(employee_profile)

    # Create a DataFrame from the collected data
    df = pd.DataFrame({
        'Company Names': company_names,
        'Employee Names': employees,
        'Employee Profiles': profiles,
    })

    # Check if data was successfully collected and DataFrame was created
    if not df.empty:
        df.to_excel('linkedin_employee_info.xlsx', index=False)
        print("\nData successfully exported to 'linkedin_employee_info.xlsx'")
    else:
        print("No data found to export")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the browser session
    driver.quit()
