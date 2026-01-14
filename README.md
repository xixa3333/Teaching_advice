# NKUST Course Evaluation Auto-Filler (高科大教學評量自動填寫機器人)

![Release](https://img.shields.io/github/v/release/xixa3333/Teaching_advice)
![Downloads](https://img.shields.io/github/downloads/xixa3333/Teaching_advice/total)
![Status](https://img.shields.io/badge/Status-Active-success)

這是一個專為國立高雄科技大學（NKUST）學生設計的自動化工具。透過自動化腳本解決期末繁瑣的教學評量填寫流程，節省寶貴時間。

**無需安裝 Python 或任何程式語言，下載解壓即可使用。**

## 📂 檔案內容

下載的 ZIP 壓縮檔內應包含以下檔案：
* `自動填寫教學意見.exe`：主程式。
* `credentials.txt`：設定檔（用來輸入帳號密碼）。

## 🚀 下載與使用教學 (Usage)

### 步驟 1：下載程式
前往本專案的 **[Releases (發行版) 頁面](https://github.com/xixa3333/Teaching_advice/releases)**，下載最新的 `.zip` 壓縮檔。

### 步驟 2：解壓縮
下載後請務必 **「解壓縮」** 該檔案（不要直接在壓縮檔內執行，會讀不到設定檔）。

### 步驟 3：設定帳號密碼
1. 開啟資料夾內的 `credentials.txt`。
2. 依照以下格式填入你的資訊（第一行學號，第二行密碼）：
    ```text
    C110123456
    MyPassword123
    ```
3. 存檔並關閉。

### 步驟 4：執行
雙擊 `自動填寫教學意見.exe` 即可開始自動填寫。

> ⚠️ **常見問題**：
> * **防毒軟體警告**：由於這是個人開發的工具，沒有購買微軟數位簽章，Windows Defender 或防毒軟體可能會誤報為病毒。請選擇「仍要執行」或將其加入信任清單。
> * **卡在登入**：如果跳出 Google 圖片驗證（九宮格），請手動在跳出的瀏覽器視窗點選驗證，登入後程式會自動接手。

## ✨ 功能特色

* **全自動化**：自動登入校務系統，智慧識別評量頁面。
* **預設滿分**：將所有評量選項預設為「非常同意」（5分/最高分）。
* **批次處理**：自動連續填寫所有科目，直到無問卷為止。
