from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

# --- 設定區 ---
TARGET_URL = "https://ceq.nkust.edu.tw/"

# 初始化瀏覽器
options = webdriver.ChromeOptions()
# options.add_argument("--headless") 

# === 關鍵設定：隱藏自動化特徵 (增加通過機率) ===
options.add_argument("--disable-blink-features=AutomationControlled") 
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

browser = webdriver.Chrome(options=options)

# 讓 navigator.webdriver = undefined，欺騙 Google
browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

try:
    browser.get(TARGET_URL)

    # 檢查是否遇到伺服器錯誤
    if "伺服器錯誤" in browser.title or "Runtime Error" in browser.page_source:
        print("警告：學校網站目前發生伺服器錯誤，程式將終止。")
        browser.quit()
        exit()

    # --- 讀取帳密與登入 ---
    try:
        with open("credentials.txt", "r") as file:
            account = file.readline().strip()
            password = file.readline().strip()
    except FileNotFoundError:
        print("錯誤：找不到 credentials.txt，請建立檔案並在第一行放帳號，第二行放密碼。")
        browser.quit()
        exit()

    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'UserAccount'))).send_keys(account)
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'Password'))).send_keys(password)

    # === 自動處理 reCAPTCHA ===
    print("嘗試自動點擊 reCAPTCHA...")
    try:
        # 1. 等待並切換到 reCAPTCHA 的 iframe
        # Google reCAPTCHA 的 iframe src 通常包含 'google.com/recaptcha'
        recaptcha_iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//iframe[contains(@src, 'recaptcha')]"))
        )
        browser.switch_to.frame(recaptcha_iframe)

        # 2. 點擊勾選框 (你提供的 class 是 .recaptcha-checkbox-border)
        checkbox = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".recaptcha-checkbox-border"))
        )
        checkbox.click()
        
        # 3. 切換回主頁面
        browser.switch_to.default_content()

        # 4. 檢查是否成功 (等待勾選狀態確認，這裡不做過多等待，直接嘗試登入，失敗則轉手動)
        time.sleep(2) # 給 Google 一點時間判斷
        print("已點擊驗證框。")

    except Exception as e:
        print(f"自動點擊驗證失敗 (可能是網路慢或元素變更): {e}")
        browser.switch_to.default_content() # 確保切回來

    # === 智慧判斷：如果跳出圖片題，則暫停讓使用者手動 ===
    # 判斷登入按鈕是否可點擊，或者頁面是否跳轉
    print("如果不幸跳出圖片九宮格，請手動完成...")
    
    # 這裡我們不使用 input() 卡死，而是直接嘗試點登入
    # 如果還沒過驗證，通常點登入會沒反應或出現提示，這裡簡化處理
    
    # 按下登入
    try:
        login_btn = browser.find_element(By.ID, 'Password')
        login_btn.send_keys(Keys.RETURN)
    except:
        pass

    # --- 進入評量頁面 (驗證是否登入成功) ---
    try:
        # 增加等待時間，如果你正在手解圖片題，這裡會等到你解完並進入頁面
        treeview = WebDriverWait(browser, 60).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'treeview'))
        )
        print("登入成功！開始執行填寫...")
        treeview.click()
        
        menu_open = WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.treeview-menu')))
        menu_open.click()
    except TimeoutException:
        print("登入超時或失敗。請確認帳號密碼，或是否被 reCAPTCHA 圖片題卡住。")
        browser.quit()
        exit()

    # --- 自動填寫迴圈 ---
    while True:
        try:
            # 等待「填寫」按鈕出現 (藍色按鈕)
            fill_button = WebDriverWait(browser, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn.btn-info'))
            )
            fill_button.click()
            print("進入新的評量頁面...")

            # === 優化重點：自動點擊所有「非常同意」 ===
            # 假設非常同意的 radio button value 包含 '5' 或者 ID 結尾是 '_5'
            # 這裡使用 XPath 尋找所有 ID 結尾為 _5 的 input 元素
            
            # 等待題目加載
            WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.TAG_NAME, "table")))
            
            # 策略：找到所有 Radio Button，並篩選出我們要選的
            # 這裡示範：點擊所有題目中「最後一個選項」(通常是非常同意)
            
            # 獲取所有題目的列 (Tr)
            questions = browser.find_elements(By.CSS_SELECTOR, "table tbody tr")
            
            for q in questions:
                try:
                    # 在每一行中，找到所有的 radio inputs
                    radios = q.find_elements(By.TAG_NAME, "input")
                    if radios:
                        # 點擊該題的最後一個選項 (通常是5分)
                        # 如果你要全部點 5 分，就是 radios[-1].click()
                        # 如果你要點 1 分，就是 radios[0].click()
                        
                        target_radio = radios[-1] # 選最後一個 (通常是最高分)
                        
                        # 使用 JavaScript 點擊 (比 ActionChains 更穩定，不會被遮擋)
                        browser.execute_script("arguments[0].click();", target_radio)
                        
                except Exception as e:
                    continue # 略過非題目的行

            print("本頁題目填寫完成，準備送出...")
            
            # 點擊送出 (藍色 Primary 按鈕)
            submit_btn = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn.btn-primary'))
            )
            browser.execute_script("arguments[0].click();", submit_btn)
            
            # 處理 alert 視窗 (如果有確認視窗)
            try:
                WebDriverWait(browser, 3).until(EC.alert_is_present())
                alert = browser.switch_to.alert
                alert.accept()
            except:
                pass

            time.sleep(2) # 稍作休息避免被 Server 踢掉

        except TimeoutException:
            print("找不到更多可填寫的問卷，或是載入超時。任務結束。")
            break
        except Exception as e:
            print(f"發生未預期錯誤: {e}")
            break

finally:
    print("關閉瀏覽器")
    browser.quit()