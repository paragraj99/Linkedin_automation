import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

# Start a new browser session
driver = webdriver.Chrome()

try:
    # Open LinkedIn and log in manually
    driver.get('https://www.linkedin.com')

    # Configure your LinkedIn username and password
    linkedin_username = input("Please enter your Email or Mobile No. : ")
    linkedin_password = input("Please enter your Password : ")

    # Log in to LinkedIn
    username_field = driver.find_element(By.ID, "session_key")
    password_field = driver.find_element(By.ID, "session_password")
    username_field.send_keys(linkedin_username)
    password_field.send_keys(linkedin_password)
    password_field.send_keys(Keys.RETURN)

    wait = WebDriverWait(driver, 20)
    wait.until(EC.url_contains("feed"))

    # Perform a search
    search_query = input("Please enter your Search query : ")
    driver.get(f"https://www.linkedin.com/search/results/companies/?keywords={search_query}")

    # Initialize lists to store company information
    all_company_names = []
    all_company_types = []
    all_company_urls = []
    all_company_sizes = []
    all_company_websites = []

    num_pages_to_search = int(input("Please enter the Page No. to get Companies data : "))
    for page_num in range(1, num_pages_to_search + 1):
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

                    company_website = "Website not avilable"

                    # Click on the company name to open its page
                    company_name_element.click()
                    time.sleep(3)  # Adjust delay as needed

                    # Find and extract the number of employees information from the company page
                    try:
                        # Get the URL of the company page
                        company_url = driver.current_url  # Fetch current URL
                        all_company_urls.append(company_url)

                        # Find the number employee
                        employees_element = driver.find_element(By.CSS_SELECTOR, ".link-without-visited-state:not(:hover).t-black--light")
                        num_employee = employees_element.text.strip()
                        all_company_sizes.append(num_employee)

                        # Find the dropdown trigger to open the dropdown
                        dropdown_trigger = driver.find_element(By.CSS_SELECTOR, '.artdeco-button--circle.artdeco-button--1')
                        dropdown_trigger.click()
                        time.sleep(2)

                        try:
                            # Find the "Visit Website" option and extract the link
                            visit_website_option = driver.find_element(By.LINK_TEXT, 'Visit website')
                            visit_website_option.click()
                            time.sleep(2)

                            # Switch to the company's website tab
                            for handle in driver.window_handles:
                                if handle != main_window_handle:
                                    driver.switch_to.window(handle)
                                    break

                            # Get the current URL which should be the company website
                            company_website = driver.current_url
                            all_company_websites.append(company_website)

                            # Close the company's website tab and switch back to the LinkedIn search tab
                            driver.close()
                            driver.switch_to.window(main_window_handle)

                        except selenium.common.exceptions.NoSuchElementException as e:
                            all_company_websites.append("Website not available")

                        # Go back to the search results page
                        driver.back()
                        time.sleep(3)  # Adjust delay as needed

                    except selenium.common.exceptions.NoSuchElementException as e:
                        all_company_sizes.append("Information not available")

                    print()
                    # Print collected data for company
                    print(f"Collected data No. {idx}) Company: {company_name} | Type: {company_type} | Url: {company_url} | Size: {num_employee} | Website: {company_website}")
                    print()

                    # Navigate back to the search results page
                    driver.execute_script("window.history.go(-1)")
                    time.sleep(3)  # Adjust delay as needed
                except Exception as e:
                    print(f"An error occurred while processing company {idx}: {e}")
                    continue

            # Construct URL for the next page
            next_page_url = f"https://www.linkedin.com/search/results/companies/?keywords=it%20services%20and%20consulting&sid=sQ9&page={page_num + 1}"

            # Navigate to the next page directly by modifying the URL
            driver.get(next_page_url)
            time.sleep(5)  # Adjust this time according to page load speed

        except selenium.common.exceptions.StaleElementReferenceException:
            print("Stale Element Reference Exception occurred. Retrying...")
            continue

    # Initialize additional lists with default values to maintain uniform lengths
    default_value = "N/A"  # You can adjust this default value as needed

    all_company_names = all_company_names[:min(len(all_company_names), len(all_company_urls))]
    all_company_types = all_company_types[:min(len(all_company_types), len(all_company_urls))]
    all_company_sizes = all_company_sizes[:min(len(all_company_sizes), len(all_company_urls))]
    all_company_websites = all_company_websites[:min(len(all_company_websites), len(all_company_urls))]
    all_company_urls = all_company_urls[:min(len(all_company_urls), len(all_company_names))]

    # Create a DataFrame from the collected data
    df = pd.DataFrame({
        'Company Names': all_company_names,
        'Company Types': all_company_types,
        'Company Urls' : all_company_urls,
        'Company Sizes': all_company_sizes,
        'Company Websites' : all_company_websites
    })

    # Export data to Excel
    df.to_excel('linkedin_company_info.xlsx', index=False)
    print("Data successfully exported to 'linkedin_company_info.xlsx'")

except selenium.common.exceptions.TimeoutException as e:
    print(f"Timeout occurred: {e}")
    # You can add handling or retry mechanism here

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the browser session
    driver.quit()