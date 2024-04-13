import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
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
    # Open LinkedIn and log in manually
    driver.get('https://www.linkedin.com')

    wait = WebDriverWait(driver, 20)
    # wait.until(EC.url_contains("feed"))

    # Perform a search
    search_query = "investment banking"
    # search_query = input("Please enter your Search query : ")

    # start_page = 15
    start_page = int(input("Please enter the start Page No. to get Companies data : "))
    # num_pages_to_search = 15  # Set the number of pages to search
    num_pages_to_search = int(input("Please enter the last Page No. to get Companies data : "))

    driver.get(f"https://www.linkedin.com/search/results/companies/?keywords={search_query}&origin=SWITCH_SEARCH_VERTICAL&page={start_page}&sid=~Sb")

    # Initialize lists to store company information
    all_company_names = []
    all_company_types = []
    all_company_urls = []
    all_company_sizes = []
    all_company_websites = []

    for page_num in range(start_page, num_pages_to_search + 1):
        try:
            # Find and store the identifiers of company elements on each page
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.reusable-search__result-container')))
            company_elements = driver.find_elements(By.CSS_SELECTOR, '.reusable-search__result-container')

            # Store the main LinkedIn window handle
            main_window_handle = driver.current_window_handle

            # Iterate through each company element on the current page
            for idx, company in enumerate(company_elements, start=1):
                try:
                    # Find and store the identifiers of company elements on each iteration
                    company_elements = driver.find_elements(By.CSS_SELECTOR, '.reusable-search__result-container')
                    current_company = company_elements[idx - 1]

                    # Extract company name from the current element
                    company_name_element = current_company.find_element(By.CSS_SELECTOR, '.entity-result__title-text')
                    company_name = company_name_element.text.strip()
                    all_company_names.append(company_name)

                    # Extract company type from the current element
                    company_type_element = current_company.find_element(By.CSS_SELECTOR, '.entity-result__primary-subtitle')
                    company_type = company_type_element.text.strip()
                    all_company_types.append(company_type)

                    # Click on the company name to open its page
                    company_name_element.click()
                    time.sleep(3) 

                    # Find and extract the number of employees information from the company page
                    try:
                        # Get the URL of the company page
                        company_url = driver.current_url  # Fetch current URL
                        all_company_urls.append(company_url)

                        # Find the number employee
                        employees_element = driver.find_element(By.CSS_SELECTOR, ".link-without-visited-state:not(:hover).t-black--light")
                        num_employee = employees_element.text.strip()
                        all_company_sizes.append(num_employee)

                        try:
                            # Find the visit website directly with first option
                            visit_website_1 = driver.find_element(By.LINK_TEXT, 'Visit website')
                            company_website_1 = visit_website_1.get_attribute("href")    
                            all_company_websites.append(company_website_1)
                            print("test weblink_1 : " , company_website_1)

                        except selenium.common.exceptions.NoSuchElementException as e:
                            # all_company_websites.append(company_website)
                            time.sleep(5)
                            # Find the dropdown trigger to open the dropdown
                            dropdown_trigger = driver.find_element(By.CSS_SELECTOR, '.artdeco-button--circle.artdeco-button--1')
                            dropdown_trigger.click()
                            time.sleep(2)

                            # Find the "Visit Website" option and extract the link
                            visit_website_option = driver.find_element(By.LINK_TEXT, 'Visit website')

                            # Collecting link
                            company_website = visit_website_option.get_attribute("href")    
                            all_company_websites.append(company_website)
                            print("test weblink : " , company_website)
                        
                        except selenium.common.exceptions.NoSuchElementException as e:
                            time.sleep(15)
                            element = driver.find_element(By.LINK_TEXT, 'About')
                            element.click() 
                            
                            # Scroll down to the bottom of the page to load more content
                            last_height = driver.execute_script("return document.body.scrollHeight")
                            while True:
                                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                                time.sleep(5)  # Adjust the sleep time as needed
                                new_height = driver.execute_script("return document.body.scrollHeight")
                                if new_height == last_height:
                                    break
                                last_height = new_height
                                time.sleep(5)

                            # Find the element by class name
                            element = driver.find_element(By.CLASS_NAME, "overflow-hidden")
                            
                            # Find the <a> tag within the element
                            link_element = element.find_element(By.TAG_NAME, "a")
                            
                            # Extract the href attribute from the <a> tag
                            href_link = link_element.get_attribute("href")
                            all_company_websites.append(href_link)
                            
                            # Print the extracted href link
                            print("Href link:", href_link)

                            # Go back to the search results page
                            # driver.back()
                        time.sleep(5)  # Adjust delay as needed
                            
                    except selenium.common.exceptions.NoSuchElementException as e:
                        all_company_websites.append("Information not available")

                    # Print collected data for company
                    print(f"Collected data No. {idx}) Company: {company_name} | Type: {company_type} | Url: {company_url} | Size: {num_employee} | Website: {company_website_1}")

                    # Navigate back to the search results page
                    driver.execute_script("window.history.go(-1)")
                    time.sleep(3)  # Adjust delay as needed
                except Exception as e:
                    print(f"An error occurred while processing company {idx}: {e}")
                    all_company_types.append("Information not available")
                    all_company_urls.append("Information not available")
                    all_company_sizes.append("Information not available")
                    all_company_websites.append("Information not available")
                    continue

            # Construct URL for the next page
            next_page_url = f"https://www.linkedin.com/search/results/companies/?keywords={search_query}&origin=SWITCH_SEARCH_VERTICAL&page={page_num + 1}&sid=~Sb"
            # Navigate to the next page directly by modifying the URL
            driver.get(next_page_url)
            time.sleep(5)  # Adjust this time according to page load speed

        except selenium.common.exceptions.StaleElementReferenceException:
            print("Stale Element Reference Exception occurred. Retrying...")
            continue

    # Initialize additional lists with default values to maintain uniform lengths
    default_value = "N/A"  # You can adjust this default value as needed

    # Truncate lists to match the length of the shortest list
    min_length = min(len(all_company_names), len(all_company_types), len(all_company_urls), len(all_company_sizes), len(all_company_websites))

    all_company_names = all_company_names[:min_length]
    all_company_types = all_company_types[:min_length]
    all_company_urls = all_company_urls[:min_length]
    all_company_sizes = all_company_sizes[:min_length]
    all_company_websites = all_company_websites[:min_length]

    # Create a DataFrame from the collected data
    df = pd.DataFrame({
        'Company Names': all_company_names,
        'Company Types': all_company_types,
        'Company Urls' : all_company_urls,
        'Company Sizes': all_company_sizes,
        'Company Websites' : all_company_websites
    })

    # Check if data was successfully collected and DataFrame was created
    if not df.empty:
        df.to_excel('linkedin_company_info.xlsx', index=False)
        print("\nData successfully exported to 'linkedin_company_info.xlsx'")
    else:
        print("No data found to export.")

except selenium.common.exceptions.TimeoutException as e:
    print(f"Timeout occurred: {e}")
    # You can add handling or retry mechanism here

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the browser session
    driver.quit()

