from ast import arg
from turtle import title
from xmlrpc.client import Boolean, boolean
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import tkinter as tk
from selenium.webdriver.common.by import By
from .forms import SearchForm
import time

# Create your views here.

@csrf_exempt
def get_name(request):
    form = SearchForm()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            text = form['look'].value()
            form = SearchForm()
            username = "duysimple98@gmail.com"
            password = "adminbkh123"
            chrome_options = Options()

            # tách chrome
            # chrome_options.add_experimental_option("detach", True)
            #chrome_options.headless = True

            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--window-size=1920,1080")

            # turn off infobar
            chrome_options.add_experimental_option(
                "excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option(
                'useAutomationExtension', False)

            chrome_options.add_experimental_option("prefs", {
                "download.prompt_for_download": False,
                "safebrowsing.enabled": True
            })

            driver = webdriver.Chrome(
                ChromeDriverManager().install(), options=chrome_options)

            # driver.maximize_window()

            driver.get("https://lovepik.com/")

            driver.find_element(By.CLASS_NAME, "btn-login").click()

            driver.find_element(
                By.XPATH, '//form[@id="form-login-v4"]//*[@name="email"]').send_keys(username)
            driver.find_element(
                By.XPATH, '//form[@id="form-login-v4"]//*[@name="password"]').send_keys(password)

            driver.find_element(By.XPATH, '//button[text()="Login "]').click()

            time.sleep(2)

            driver.switch_to.window(driver.window_handles[0])


            try:
                elem = driver.find_element(By.XPATH, '//i[@class="iconfont icon-guanbitubiao btn-close-login-sign"]')
                if elem.is_displayed():
                    elem.click()
                    print("Có phần tử xuất hiện")
            except NoSuchElementException:
                print("Không tìm thấy phần tử")

            driver.execute_script("window.open('about:blank', 'secondtab');")
            driver.switch_to.window("secondtab")
            driver.get(text)

            time.sleep(2)

            # driver.find_element(
            #     By.XPATH, '//div[@class="down_box"]//*[@class="pub psd"]').click()

            try:
                psd = driver.find_element(By.XPATH, '//div[@class="down_box"]//*[@class="pub psd"]')
                # jpg = driver.find_element(By.XPATH, '//div[@class="down_box"]//*[@class="pub jpg copyDownTips"]')
                if psd.is_displayed():
                    psd.click()
                    print("Đây là file PSD")
            except NoSuchElementException:
                try:
                    jpg = driver.find_element(By.XPATH, '//div[@class="down_box"]//*[@class="pub jpg copyDownTips"]')
                    if jpg.is_displayed():
                        jpg.click()
                        print("Đây là file JPG")
                except NoSuchElementException:
                    try:
                        combo = driver.find_element(By.XPATH, '//div[@class="pub jpg_psd"]//*[@class="pub_s psd_s"]')
                        if combo.is_displayed():
                            combo.click()
                            print("Đây là link 2 nút")
                    except NoSuchElementException:
                        print("Không tìm thấy bất kỳ phần tử nào")
                        content = "Link bạn nhập sai yêu cầu. Vui lòng kiểm tra lại."
                        return render(request, "index.html", {'form': form, 'link': content})

            time.sleep(2)

            driver.switch_to.window(driver.window_handles[1])

            print(driver.current_url)

            try:
                close_download = driver.find_element(By.XPATH, '//span[@class="btn_close act_lazy"]')
                if close_download.is_displayed():
                    close_download.click()
                    print("Có phần tử xuất hiện")
            except NoSuchElementException:
                print("Không tìm thấy phần tử")

            # driver.find_element(
            #     By.XPATH, '//span[@class="btn_close act_lazy"]').click()

            time.sleep(2)

            # try:
            #     s = driver.find_element(By.XPATH, '//span[@class="copy-span"]').click()
            #     print("Copied")
            # except:
            #     print("Error Copy")

            content = driver.find_element(
                By.XPATH, '//input[@class="copy-ipt link"]').get_attribute("value")

            # root = tk.Tk()
            # copied = root.clipboard_get()

            print("Link download là: ", content)

            driver.quit()
            return render(request, "index.html", {'form': form, 'link': content})

    args = {'form': form}
    return render(request, 'index.html', args)
