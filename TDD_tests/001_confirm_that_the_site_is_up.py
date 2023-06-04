from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome()
driver.maximize_window()
options = webdriver.ChromeOptions()
options.headless = False
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

# Locators
B_THREE = (By.XPATH, "//img[@name='space62']")
C_FOUR_1 = (By.XPATH, "//img[@name='space53']")
C_FOUR_2 = (By.XPATH, "//img[@onclick='didClick(5, 3)']")
MAKE_A_MOVE = EC.visibility_of_element_located((By.XPATH, "//p[@id='message']"))
D_FIVE = (By.XPATH, "//img[@name='space44']")

# Explicit wait
wait = WebDriverWait(driver, 15)

# 1. Open the url
driver.get('https://www.gamesforthebrain.com/game/checkers/')
# 1.1. Make a screenshot if 'options.headless = True' it fits the screen
# driver.get_screenshot_as_file('site_is_up.png')
S = lambda X: driver.execute_script('return document.body.parentNode.scroll' + X)
driver.set_window_size(S('Width'),S('Height'))
driver.find_element(By.TAG_NAME, 'body').screenshot('site_is_up.png')
# 1.2. Verify the url 'https://www.gamesforthebrain.com/game/checkers/' is here
expected_url = 'https://www.gamesforthebrain.com/game/checkers/'
actual_url = driver.current_url
if expected_url in actual_url:
    print(f'Expected "{expected_url}", and got: "{actual_url}"\n')
else:
    print(f'Expected "{expected_url}", but got: "{actual_url}"\n')

# 2. Move one. Go B3 -> C4
wait.until(EC.element_to_be_clickable(B_THREE)).click()
wait.until(EC.element_to_be_clickable(C_FOUR_1)).click()
# 2.1. Make a screenshot if 'options.headless = True' it fits the screen
# driver.get_screenshot_as_file('move_one_b3_c4.png')
S = lambda X: driver.execute_script('return document.body.parentNode.scroll' + X)
driver.set_window_size(S('Width'),S('Height'))
driver.find_element(By.TAG_NAME, 'body').screenshot('move_one_b3_c4.png')

# 3. Verify "Make a move." is here
make_a_move_expected_text = 'Make a move.'
sleep(1) # EC and explicit wait do not work here. Your app is just more than raw.
make_a_move_actual_text = wait.until(MAKE_A_MOVE).text
if make_a_move_expected_text in make_a_move_actual_text:
    print(f'Expected "{make_a_move_expected_text}", and got: "{make_a_move_actual_text}"\n')
else:
    print(f'Expected "{make_a_move_expected_text}", but got: "{make_a_move_actual_text}"\n')
# 3.1. Make a screenshot if 'options.headless = True' it fits the screen
# driver.get_screenshot_as_file('make_a_move.png')
S = lambda X: driver.execute_script('return document.body.parentNode.scroll' + X)
driver.set_window_size(S('Width'),S('Height'))
driver.find_element(By.TAG_NAME, 'body').screenshot('make_a_move.png')


# 4. Move two. Go C4 -> D5 # Your app does nog go beyond previous step.
# wait.until(EC.element_to_be_clickable(C_FOUR_2)).click()
menu = driver.find_element(By.XPATH, "//img[@onclick='didClick(5, 3)']")
actions = ActionChains(driver)
actions.move_to_element(menu)
actions.click(menu)
actions.perform()
# wait.until(EC.element_to_be_clickable(D_FIVE)).click()
menu = driver.find_element(By.XPATH, "//img[@name='space44']")
actions = ActionChains(driver)
actions.move_to_element(menu)
actions.click(menu)
actions.perform()

# Driver close
# driver.close()

# # Sleep to see what we have
sleep(300)
# 60 sek is not enough. Your app is hanging up in status "Please wait."
# if options.headless = False
# for more 300 sek not responding on step 4.
# Thus I do not have a valid reason and a base to automate your app.
# See demo: https://github.com/lupusludensest/18wheelerschool_06_apr_2023-what I can do in UI,
# e2e automation with BDD, Selenium WD, Allure.

# Driver quit
# driver.quit()