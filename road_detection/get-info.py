from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import requests
import os
import time

def download_google_images(query, num_images):
    # Set up the Selenium driver
    driver = webdriver.Chrome(ChromeDriverManager().install())

    # Go to Google Images
    driver.get(f"https://www.google.com/search?q={query}&tbm=isch")

    # Create directory for the images
    if not os.path.exists(query):
        os.makedirs(query)
    
    # Scroll down the page to load more images
    scroll_down(driver)

    # Find all img elements
    img_tags = driver.find_elements_by_css_selector('.rg_i.Q4LuWd')

    # Download the number of images specified
    count = 0
    for i, img in enumerate(img_tags):
        # Get the image URL
        img_url = img.get_attribute('data-src')

        # Download the image
        if img_url is not None:
            try:
                img_data = requests.get(img_url).content
                with open(f'{query}/{count}.jpg', 'wb') as handler:
                    handler.write(img_data)
                
                count += 1

                if count >= num_images:
                    break
            except:
                print(f'Error downloading image {img_url}')

    driver.quit()

def scroll_down(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Wait for some time for the new images to load
        time.sleep(2)

        # Calculate the new height of the page
        new_height = driver.execute_script("return document.body.scrollHeight")

        # Break the loop if no more images are loaded
        if new_height == last_height:
            break
        
        last_height = new_height

download_google_images('ontario speed limit signs only', 1000)
