import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from openpyxl import Workbook

# Configure your LinkedIn username and password
linkedin_username = "yourmail@gmail.com"
linkedin_password = "your_password"

# Create a new instance of the Chrome driver
driver = webdriver.Chrome()

# Navigate to LinkedIn
driver.get("https://www.linkedin.com")

# Log in to LinkedIn
username_field = driver.find_element(By.ID, "session_key")
password_field = driver.find_element(By.ID, "session_password")
username_field.send_keys(linkedin_username)
password_field.send_keys(linkedin_password)
password_field.send_keys(Keys.RETURN)

# Use WebDriverWait instead of time.sleep
wait = WebDriverWait(driver, 10)
wait.until(EC.url_contains("feed"))

search_criteria = input("Enter your search criteria (e.g., 'IT services and consulting'): ")

# Navigate to the company search page
driver.get("https://www.linkedin.com/search/results/companies/")
search_query = "it services and consulting"
driver.get(f"https://www.linkedin.com/search/results/companies/?keywords={search_query}")

# Find the search input and enter the user's search criteria
search_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='Search for companies']")))
search_input.send_keys("IT services and consulting")
search_input.send_keys(Keys.RETURN)

# Wait for the search results to load using WebDriverWait
wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".reusable-search__result-container")))

# Create a new Excel workbook
workbook = Workbook()
sheet = workbook.active

# Find and extract search results
search_results = driver.find_elements(By.CSS_SELECTOR, ".reusable-search__result-container")

for result in search_results:
    company_name = result.find_element(By.CSS_SELECTOR, ".entity-result__title-text").text
    industry = result.find_element(By.CSS_SELECTOR, ".entity-result__primary-subtitle").text
    location = result.find_element(By.CSS_SELECTOR, ".entity-result__secondary-subtitle").text
    sheet.append([company_name, industry, location])

# Save the Excel file
workbook.save("linkedin_data.xlsx")

# Close the web browser
driver.close()