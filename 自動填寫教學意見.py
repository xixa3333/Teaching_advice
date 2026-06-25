from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
import time

# --- 設定區 ---
TARGET_URL = "https://ceq.nkust.edu.tw/"

# 舊版精確的按鈕 ID 清單
TARGET_IDS = [
    '11_1', '12_1', '13_1', '14_1', '15_1', '16_1',
    '21_5', '22_5', '23_1', '24_1',
    '31_5', '32_5', '33_5',
    '41_5', '42_5', '43_5',
    '51_5', '52_5', '53_5',
    '61_5', '62_5', '63_5',
    '71_5',
    '81_2', '82_3'
]

options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled") 
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

browser = webdriver.Chrome(options=options)
browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

def ClickElementByJS(element):
    """使用 JavaScript 執行點擊 (用於填寫問卷選項與送出)"""
    browser.execute_script("arguments[0].click();", element)

# --- 1. 登入控制主迴圈 ---
while True:
    try:
        browser.get(TARGET_URL)

        if "伺服器錯誤" in browser.title or "Runtime Error" in browser.page_source:
            print("學校網站目前發生伺服器錯誤，5秒後重試...")
            time.sleep(5)
            continue

        try:
            with open("credentials.txt", "r") as file:
                account = file.readline().strip()
                password = file.readline().strip()
        except FileNotFoundError:
            print("錯誤：找不到 credentials.txt，請建立檔案。")
            browser.quit()
            exit()

        # 填寫帳密
        account_field = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'UserAccount')))
        account_field.clear()
        account_field.send_keys(account)

        password_field = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'Password')))
        password_field.clear()
        password_field.send_keys(password)

        # 處理 reCAPTCHA
        print("嘗試自動點擊 reCAPTCHA 勾選框...")
        try:
            recaptcha_iframe = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, "//iframe[contains(@src, 'recaptcha')]"))
            )
            browser.switch_to.frame(recaptcha_iframe)
            
            checkbox = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".recaptcha-checkbox-border")))
            checkbox.click()
            
            print("請在瀏覽器上手動完成圖片九宮格驗證（若有的話）...")
            WebDriverWait(browser, 120).until(
                lambda d: d.find_element(By.ID, "recaptcha-anchor").get_attribute("aria-checked") == "true"
            )
            print("reCAPTCHA 驗證成功，準備登入。")
            
        except Exception as e:
            print(f"驗證碼監聽異常或超時: {e}")
        finally:
            browser.switch_to.default_content()

        # 送出表單
        password_field = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'Password')))
        password_field.send_keys(Keys.RETURN)

        # 【核心修正】嚴格限制判定範圍：只要看得到側邊欄元素，就代表登入成功，立刻斷開重試迴圈
        WebDriverWait(browser, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'treeview'))
        )
        print("登入成功！")
        break 

    except TimeoutException:
        print("\n[偵測到登入失敗] 密碼錯誤或驗證碼逾時。程式將自動重試...\n")
        time.sleep(2)
        continue

# --- 2. 進入評量頁面 (移到迴圈外，確保不干擾登入判定) ---
print("開始導覽至問卷頁面...")
try:
    # 回復舊版 ActionChains 模擬人類點擊，確保觸發側邊欄展開事件
    treeview_btn = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'treeview'))
    )
    ActionChains(browser).move_to_element(treeview_btn).click().perform()
    
    # 點擊展開後的子選單
    menu_open = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.treeview-menu.menu-open'))
    )
    ActionChains(browser).move_to_element(menu_open).click().perform()
    print("成功進入問卷填寫區！")
except Exception as e:
    print(f"導覽選單時發生動畫延遲，將嘗試直接尋找填寫按鈕... (偵測訊息: {e})")

# --- 3. 自動填寫問卷迴圈 ---
while True:
    try:
        # 等待並點擊「填寫」按鈕 (藍色按鈕)
        fill_button = WebDriverWait(browser, 8).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn.btn-info'))
        )
        ClickElementByJS(fill_button)
        print("進入新的評量頁面...")

        # 依序等待並點擊舊版指定的每一個精確 ID
        for element_id in TARGET_IDS:
            button = WebDriverWait(browser, 8).until(
                EC.presence_of_element_located((By.ID, element_id))
            )
            ClickElementByJS(button)
        
        print("本頁特定題目填寫完成，準備送出...")
        
        # 點擊送出按鈕 (藍色 Primary 按鈕)
        submit_btn = WebDriverWait(browser, 8).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn.btn-primary'))
        )
        ClickElementByJS(submit_btn)
        
        # 處理確認彈窗 (Alert)
        try:
            WebDriverWait(browser, 3).until(EC.alert_is_present())
            browser.switch_to.alert.accept()
        except:
            pass

        time.sleep(2.5) # 稍微停頓避免請求過快被伺服器阻擋

    except TimeoutException:
        print("已填寫完畢，或找不到更多可填寫的問卷。")
        break
    except Exception as e:
        print(f"填寫期間發生未預期錯誤: {e}")
        break

print("所有任務結束，5秒後關閉瀏覽器")
time.sleep(5)
browser.quit()