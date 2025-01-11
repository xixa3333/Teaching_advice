from selenium.webdriver.common.keys import Keys  # 確保正確導入 Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.common.exceptions import TimeoutException

def UseIDBotton(ID):
    button = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, ID))
    )
    action = ActionChains(browser)
    action.move_to_element(button).click().perform()

# 從檔案讀取帳號和密碼
with open("credentials.txt", "r") as file:
    account = file.readline().strip()  # 第一行是帳號
    password = file.readline().strip()  # 第二行是密碼

# 初始化瀏覽器
browser = webdriver.Chrome()
browser.get("https://ceq.nkust.edu.tw/")

# 填寫帳號和密碼
element = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.ID, 'UserAccount'))
)
element.send_keys(account)

element = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.ID, 'Password'))
)
element.send_keys(password)

# 手動完成 reCAPTCHA 後提交表單
input("請先手動完成 reCAPTCHA 驗證，然後再按 Enter 繼續...")
element.send_keys(Keys.RETURN)

button = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'treeview'))
)
action = ActionChains(browser)
action.move_to_element(button).click().perform()

button = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '.treeview-menu.menu-open'))
)
action = ActionChains(browser)
action.move_to_element(button).click().perform()

while(True):
    try:
        # 等待並點擊 .btn.btn-info
        button = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.btn.btn-info'))
        )
        action = ActionChains(browser)
        action.move_to_element(button).click().perform()

        # 點擊所有 ID 按鈕
        UseIDBotton('11_1')
        UseIDBotton('12_1')
        UseIDBotton('13_1')
        UseIDBotton('14_1')
        UseIDBotton('15_1')
        UseIDBotton('16_1')
        UseIDBotton('21_5')
        UseIDBotton('22_5')
        UseIDBotton('23_1')
        UseIDBotton('24_1')
        UseIDBotton('31_5')
        UseIDBotton('32_5')
        UseIDBotton('33_5')
        UseIDBotton('41_5')
        UseIDBotton('42_5')
        UseIDBotton('43_5')
        UseIDBotton('51_5')
        UseIDBotton('52_5')
        UseIDBotton('53_5')
        UseIDBotton('61_5')
        UseIDBotton('62_5')
        UseIDBotton('63_5')
        UseIDBotton('71_5')
        UseIDBotton('81_2')
        UseIDBotton('82_3')

        # 等待並點擊 .btn.btn-primary
        button = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.btn.btn-primary'))
        )
        action = ActionChains(browser)
        action.move_to_element(button).click().perform()

    except TimeoutException:
        print("已填寫完畢")
        break
    
time.sleep(5)
browser.quit()
