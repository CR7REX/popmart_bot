import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys

def popmart_bot(product_url, email, password, pick_up_location=None):
    
    # Initialize the Chrome driver
    options = uc.ChromeOptions()
    options.add_argument("--no-first-run --no-service-autorun --password-store=basic")

    driver = uc.Chrome(options=options, detach=True)

    # go to site
    driver.get("https://www.popmart.com/us/user/login")

    # wait and click
    WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.XPATH, "//div[text()='ACCEPT']"))
    ).click()

    # Entering email and click continue button
    email_input = driver.find_element(By.ID, "email")
    email_input.send_keys(email)
    WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'CONTINUE')]"))
    ).click()
    time.sleep(1.2)

    # Entering password and click sign in button
    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys(password)
    WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'SIGN IN')]"))
    ).click()
    time.sleep(1.2)

    # Go to the product page
    driver.get(product_url)

    # Select Pick Up location
    if not pick_up_location:
        pick_up_location = "Victoria Gardens POP-UP"
    WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.XPATH, f"//div[text()='{pick_up_location}']"))
    ).click()
    time.sleep(1.2)

    # Wait for user's input to start
    input("⏳ Login successful. Press Enter to start...")

    # Check the button status
    add_to_bag_button = driver.find_element(By.XPATH, "//div[contains(@class, 'index_usBtn__UUQYB')]")
    start_time = time.time()
    while add_to_bag_button.text != "ADD TO BAG":
        if time.time() - start_time > 600:
            print("⏰ Timeout reached. Exiting loop.")
            driver.quit()
            return False
        time.sleep(0.5)
        driver.refresh()
        time.sleep(1.5)
        add_to_bag_button = driver.find_element(By.XPATH, "//div[contains(@class, 'index_usBtn__UUQYB')]")

    add_to_bag_button.click()


    # Go to store pickup shopping bag
    shopping_bag_button = driver.find_element(By.XPATH, "//div[contains(@class, 'index_cartItem__xumFD')]")
    shopping_bag_button.click()
    WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'STORE PICKUP')]"))
    ).click()
    time.sleep(1.2)


    # CLick the "CONFIRM AND CHECKOUT" button
    WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.XPATH, "//button[span[contains(text(), 'CONFIRM AND CHECK OUT')]]"))
    ).click()
    time.sleep(1.2)

    # CLick the "PROCEED TO PAY" button
    WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'PROCEED TO PAY')]"))
    ).click()
    time.sleep(0.8)

    # Click "CONFIRM" if popup appears
    try:
        confirm_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'CONFIRM')]"))
        )
        time.sleep(0.5)
        confirm_button.click()
    except Exception as e:
        print("No confirmation button found or not clickable.")

    input("✅ Script completed. Press Enter to exit...")
    driver.quit()
    return True

if __name__ == "__main__":
    product_url = sys.argv[1]
    email = sys.argv[2]
    password = sys.argv[3]
    pick_up_location = sys.argv[4]
    popmart_bot(product_url, email, password, pick_up_location)