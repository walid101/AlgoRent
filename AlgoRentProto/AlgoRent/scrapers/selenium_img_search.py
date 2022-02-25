from selenium import webdriver

DRIVER = 'chromedriver'
driver = webdriver.Chrome(DRIVER)
img = driver.get('https://www.redfin.com/NY/Flushing/32-22-204th-St-11361/home/20833767')
print(img)
screenshot = driver.save_screenshot('my_screenshot.png')
driver.quit()