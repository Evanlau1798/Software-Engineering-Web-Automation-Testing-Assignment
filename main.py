import time,unittest,chromedriver_autoinstaller,pyautogui,os,json
from selenium.webdriver import ChromeOptions
from helium import *
from pynput.keyboard import Controller

class FilpClassTest(unittest.TestCase):
    def setUp(self):
        chromedriver_autoinstaller.install(cwd=True) #自動安裝chrome驅動
        options = ChromeOptions()
        options.add_argument('--blink-settings=imagesEnabled=false') #禁止圖片載入以加快執行速度並減少網路流量消耗
        self.driver = start_chrome("https://flipclass.stust.edu.tw/",options=options)
        with open('./account.json', 'r') as f: #獲取存在account.json的帳號及密碼
            data = json.load(f)
        self.account = data['account']
        self.password = data['password']
        
    def test(self):
        write(self.account,into="帳號")
        write(self.password,into="密碼 (區分大小寫)")
        click(Button("登入"))
        for _ in range(5):
            if Link("保持登入").exists(): #判斷"保持登入"按鈕是否存在，以避免重複登入之是否維持多IP登入之詢問框
                click(Link("保持登入"))
                break
            else:
                time.sleep(0.5)
        click(Link("軟體工程_四技資工三甲"))
        click(Link("作業"))
        click(Link("[加分題]測試網頁，在這裡自動上傳一個作業，並自動標註學號姓名，與自動上傳你的python code，自動繳交送出"))
        click(Link("交作業"))
        while True:
            if Button("上傳檔案").exists(): #判斷"上傳檔案"按鈕是否已載入
                time.sleep(1) #稍微等待文字輸入框載入
                break
            else:
                time.sleep(0.5)
        pyautogui.hotkey('tab','tab','tab',interval=0.1) #移動輸入位置至訊息輸入框
        Controller().type("學號:4a9g0083\n姓名:饒亮威")
        click(Button("上傳檔案"))
        self.driver.find_element_by_xpath("//input[@type='file']").send_keys(os.path.abspath('./') + "\main.py") #上傳這份python檔案
        time.sleep(1) #等待資料上傳
        click(Button("關閉"))
        click(Button("繳交"))
        return

if __name__ == '__main__':
    unittest.main()