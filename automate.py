# paragrajwaghmare@gmail.com
# king6369

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

# Start a new browser session
driver = webdriver.Chrome()

# Open LinkedIn and log in manually
driver.get('https://www.linkedin.com')



# Configure your LinkedIn username and password
linkedin_username = "paragrajwaghmare@gmail.com"
linkedin_password = "king6369"

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

input("Log in to LinkedIn and press Enter...")

# Perform a search
search_query = "it services and consulting"
driver.get(f"https://www.linkedin.com/search/results/companies/?keywords={search_query}")

# Scroll down to load more results
for _ in range(5):  # Adjust the number of scrolls based on your needs
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
    time.sleep(2)

# Extract company data
companies = driver.find_elements(By.CSS_SELECTOR, '.reusable-search__result-container')

company_data = [[
    company.find_element(By.CSS_SELECTOR, '.entity-result__title-text').text,
    company.find_element(By.CSS_SELECTOR, '.entity-result__description').text
] for company in companies]

# Export data to Excel
df = pd.DataFrame(company_data, columns=['Name', 'Description'])
df.to_excel('linkedin_companies.xlsx', index=False)

# Close the browser
driver.quit()