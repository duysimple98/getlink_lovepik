from ast import arg
from lib2to3.pgen2.pgen import PgenGrammar
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
# import tkinter as tk
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
            password = "Adminbkh123@"
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
                elem = driver.find_element(
                    By.XPATH, '//i[@class="iconfont icon-guanbitubiao btn-close-login-sign"]')
                if elem.is_displayed():
                    elem.click()
                    print("Có phần tử xuất hiện")
            except NoSuchElementException:
                print("Không tìm thấy phần tử")


            driver.execute_script("window.open('about:blank', 'secondtab');")
            driver.switch_to.window(driver.window_handles[0])
            driver.close()
            driver.switch_to.window("secondtab")
            driver.get(text)
            print("Tab đầu tiên là: ", driver.current_url)

            time.sleep(2)

            try:
                psd = driver.find_element(
                    By.XPATH, '//div[@class="down_box"]//*[@class="pub psd"]')
                if psd.is_displayed():
                    psd.click()
                    print("Đây là file PSD")
            except NoSuchElementException:
                try:
                    jpg = driver.find_element(
                        By.XPATH, '//div[@class="down_box"]//*[@class="pub jpg copyDownTips"]')
                    if jpg.is_displayed():
                        jpg.click()
                        print("Đây là file JPG")
                except NoSuchElementException:
                    try:
                        combo = driver.find_element(
                            By.XPATH, '//div[@class="pub jpg_psd"]')
                        if combo.is_displayed():
                            id = text.split("image-", 1)[1].split("/")[0]
                            print("ID của template là: ", id)
                            driver.execute_script("window.open('about:blank', 'thirdtab');")
                            driver.switch_to.window("thirdtab")
                            # driver.switch_to.window(driver.window_handles[1])
                            driver.get('https://lovepik.com/download/detail/' + id + '?byso=&type=3')
                            print("Tab thứ 2 là: ",driver.current_url )
                            try:
                                close_download = driver.find_element(
                                    By.XPATH, '//span[@class="btn_close act_lazy"]')
                                if close_download.is_displayed():
                                    close_download.click()
                                    print("Có phần tử xuất hiện")
                            except NoSuchElementException:
                                print("Không tìm thấy phần tử")
                            content_jpg = driver.find_element(By.XPATH, '//input[@class="copy-ipt link"]').get_attribute("value")

                            print("Link download JPG là: ", content_jpg)
                            driver.close()
                            driver.switch_to.window(driver.window_handles[0])
                            print("Tab hiện tại là: ", driver.current_url)
                            time.sleep(2)
                            psd_s = driver.find_element(By.XPATH, '//div[@class="pub jpg_psd"]//*[@class="pub_s psd_s"]')
                            if psd_s.is_displayed():
                                psd_s.click()
                                print("Đã lấy thành công nút")
                                print("Tab thứ 3 là: ", driver.current_url)
                                try:
                                    close_download = driver.find_element(
                                        By.XPATH, '//span[@class="btn_close act_lazy"]')
                                    if close_download.is_displayed():
                                        close_download.click()
                                        print("Ok có nút")
                                except NoSuchElementException:
                                    print("Chả thấy đâu cả")
                                time.sleep(2)
                                psd_content = driver.find_element(By.XPATH, '//input[@class="copy-ipt link"]').get_attribute("value")
                                print("Link file PSD 2 nút là: ",psd_content)
                            driver.quit()
                            return render(request, "index.html", {'form': form, 'link': content_jpg, 'psd_content': psd_content})
                            
                    except NoSuchElementException:
                        print("Không tìm thấy bất kỳ phần tử nào")
                        content = "Link bạn nhập sai yêu cầu. Vui lòng kiểm tra lại."
                        return render(request, "index.html", {'form': form, 'link': content})

            time.sleep(2)


            # driver.switch_to.window(driver.window_handles[1])

            # print("Tab hiện tại là: ", driver.current_url)
            
            # try:
            #     combo_psd = driver.find_element(By.XPATH, '//div[@class="pub jpg_psd"]')
            #     if combo_psd.is_displayed():
            #         psd_s = driver.find_element(By.XPATH, '//a[@class="pub_s psd_s"]').get_attribute("onclick")
            #         print ("PSD 2 nút có link: ",psd_s)
            #         driver.execute_script(psd_s)
            # except NoSuchElementException:
            #     print("Không tìm thấy bất kỳ phần tử nào")
            #     content = "Link bạn nhập sai yêu cầu. Vui lòng kiểm tra lại."
            #     return render(request, "index.html", {'form': form, 'link': content})


            try:
                close_download = driver.find_element(
                    By.XPATH, '//span[@class="btn_close act_lazy"]')
                if close_download.is_displayed():
                    close_download.click()
                    print("Có phần tử xuất hiện")
            except NoSuchElementException:
                print("Không tìm thấy phần tử")


            time.sleep(2)

            content = driver.find_element(
                By.XPATH, '//input[@class="copy-ipt link"]').get_attribute("value")

            # root = tk.Tk()
            # copied = root.clipboard_get()

            print("Link download là: ", content)

            driver.quit()
            return render(request, "index.html", {'form': form, 'link': content})

    args = {'form': form}
    return render(request, 'index.html', args)
