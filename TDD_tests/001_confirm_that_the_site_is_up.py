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
options.headless = True
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

# Locators
B_THREE = (By.XPATH, "//img[@name='space62']")
C_FOUR = (By.XPATH, "//img[@name='space53']")
MAKE_A_MOVE = EC.visibility_of_element_located((By.XPATH, "//p[@id='message']"))
D_FIVE = (By.XPATH, "//img[@name='space44']")
D_THREE = (By.XPATH, "//img[@onclick='didClick(4, 2)']")
B_FIVE = (By.XPATH, "//img[@name='space64']")
F_THREE = (By.XPATH, "//img[@name='space22']")
G_FOUR = (By.XPATH, "//img[@name='space13']")
E_TWO = (By.XPATH, "//img[@name='space31']")

# Explicit wait
wait = WebDriverWait(driver, 15)

# 1. Open the url
driver.get('https://www.gamesforthebrain.com/game/checkers/')
# 1.1. Make a screenshot if 'options.headless = True' it fits the screen
S = lambda X: driver.execute_script('return document.body.parentNode.scroll' + X)
driver.set_window_size(S('Width'),S('Height'))
sleep(2)
driver.find_element(By.TAG_NAME, 'body').screenshot('site_is_up.png')
# 1.2. Verify the url 'https://www.gamesforthebrain.com/game/checkers/' is here
expected_url = 'https://www.gamesforthebrain.com/game/checkers/'
actual_url = driver.current_url
if expected_url in actual_url:
    print(f'Expected "{expected_url}", and got: "{actual_url}"\n')
else:
    print(f'Expected "{expected_url}", but got: "{actual_url}"\n')
# 1.1. Make a sessionId to verify the session is opened
one_step_session_id = driver.session_id
print(f'one_step_session_id: {one_step_session_id} is opened\n')

# 2. Move one. Go B3 -> C4
wait.until(EC.element_to_be_clickable(B_THREE)).click()
wait.until(EC.element_to_be_clickable(C_FOUR)).click()
# 2.1. Make a screenshot if 'options.headless = True' it fits the screen
sleep(2)
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
sleep(2)
driver.find_element(By.TAG_NAME, 'body').screenshot('make_a_move.png')

# 4. Move two. Go C4 -> D5 # Your app does nog go beyond this step.
menu = driver.find_element(By.XPATH, "//img[@onclick='didClick(5, 3)']")
actions = ActionChains(driver)
actions.move_to_element(menu)
actions.click(menu)
sleep(2)
actions.perform()

menu = driver.find_element(By.XPATH, "//img[@name='space44']")
actions = ActionChains(driver)
actions.move_to_element(menu)
actions.click(menu)
sleep(2)
actions.perform()

# 5. Move three. Go D3 -> B5. Taking a blue piece C4.
menu = driver.find_element(By.XPATH, "//img[@onclick='didClick(4, 2)']")
actions = ActionChains(driver)
actions.move_to_element(menu)
actions.click(menu)
sleep(2)
actions.perform()

menu = driver.find_element(By.XPATH, "//img[@name='space64']")
actions = ActionChains(driver)
actions.move_to_element(menu)
actions.click(menu)
sleep(2)
actions.perform()

# 6. Move four. Go F3 -> G4.
menu = driver.find_element(By.XPATH, "//img[@onclick='didClick(2, 2)']")
actions = ActionChains(driver)
actions.move_to_element(menu)
actions.click(menu)
sleep(2)
actions.perform()

menu = driver.find_element(By.XPATH, "//img[@name='space13']")
actions = ActionChains(driver)
actions.move_to_element(menu)
actions.click(menu)
sleep(2)
actions.perform()

# 7. Move five. Go E2 -> F3.
menu = driver.find_element(By.XPATH, "//img[@name='space31']")
actions = ActionChains(driver)
actions.move_to_element(menu)
actions.click(menu)
sleep(2)
actions.perform()

menu = driver.find_element(By.XPATH, "//img[@name='space22']")
actions = ActionChains(driver)
actions.move_to_element(menu)
actions.click(menu)
sleep(2)
actions.perform()
# 7.1. Make a sessionId
seven_step_session_id = driver.session_id
print(f'seven_step_session_id: {seven_step_session_id}\n')

# 8. Restart the game after five moves.
driver.find_element(By.XPATH, "//a[text()='Restart...']").click()
driver.refresh()

# 9. Confirm that the restarting had been successful
# 9.1. Make a sessionId
nine_step_session_id = driver.session_id
print(f'nine_step_session_id: {nine_step_session_id}\n')
if one_step_session_id == seven_step_session_id == nine_step_session_id:
    print(f'Still the same session_id\n')
# 9.2. Make a screenshot if 'options.headless = True' it fits the screen
sleep(2)
driver.find_element(By.TAG_NAME, 'body').screenshot('fresh_screen_new_game.png')

# Driver close
driver.close()

# Sleep to see what we have
# sleep(300)
# See demo: https://github.com/lupusludensest/18wheelerschool_06_apr_2023-what I can do in UI,
# e2e automation with BDD, Selenium WD, Allure.

# Driver quit
driver.quit()