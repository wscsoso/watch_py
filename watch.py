from selenium import webdriver
from selenium.webdriver.common.by import By
import time

browser = webdriver.Chrome()

def isElementExist(str):
    flag=True
    try:
        browser.find_element(By.XPATH,(str))
        return flag
    except:
        flag=False
        return flag
def get_onepage():
    counts_li = len(browser.find_elements(By.XPATH,'//*[@id="J_goodsList"]/ul/li'))
    for i in range(counts_li):
        f = open("poker.csv", mode="a", encoding="utf-8")
        try:
            browser.find_element(By.XPATH,f'//*[@id="J_goodsList"]/ul/li[{i + 1}]/div/div[1]/a/img').click()
        except:
            try:
                browser.refresh()
                browser.find_element(By.XPATH,f'//*[@id="J_goodsList"]/ul/li[{i + 1}]/div/div[1]/a/img').click()
            except:
                continue
        browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(3)
        price = browser.find_element(By.XPATH,f'//*[@id="J_goodsList"]/ul/li[{i + 1}]/div/div[2]/strong/i').text.strip()
        browser.switch_to.window(browser.window_handles[-1])

        #爬取ul下所有li
        counts_ul = len(browser.find_elements(By.XPATH, '//*[@id="detail"]/div[2]/div[1]/div[1]/ul[2]/li'))
        res = []
        for j in range(counts_ul):
            # spmc 商品名称   商品毛重   血压监测  优选服务  电源方式  防水 表盘形状 适用人群
            try:
                temp = browser.find_element(By.XPATH,f'//*[@id="detail"]/div[2]/div[1]/div[1]/ul[2]/li[{j + 1}]').text.strip()
                # print(temp)
                res.append(temp)
            except:
                temp = ''

        # print(res)
        res = (','.join(str(i) for i in res))


        try:
            pl = browser.find_element(By.XPATH,'//*[@id="detail"]/div[1]/ul/li[5]')
        except:
            pl = ''

            pl.click()


        #点击评论按钮后，下拉显示出“只看当前商品评论”复选框
        browser.execute_script('window.scrollTo(0, 3000)')
        time.sleep(2)
        # dqpl 当前评论  qbpl 全部评论 st 晒图 spsd 视频晒单  zp 总评  hp好评 cp差评
        if isElementExist('//*[@id="comm-curr-sku"]'):
            try:
                dqpl = browser.find_element(By.XPATH,'//*[@id="comm-curr-sku"]')
                dqpl.click()
            except:
                browser.close()
                browser.switch_to.window(browser.window_handles[0])
                continue
        else:
            browser.refresh()
            pl = browser.find_element(By.XPATH,'//*[@id="detail"]/div[1]/ul/li[5]')
            pl.click()
            time.sleep(2)
            if isElementExist('//*[@id="comm-curr-sku"]'):

                try:
                    dqpl = browser.find_element(By.XPATH, '//*[@id="comm-curr-sku"]')
                    time.sleep(3)
                    dqpl.click()
                except:
                    browser.close()
                    browser.switch_to.window(browser.window_handles[0])
                    continue
            else:
                browser.refresh()
                pl = browser.find_element(By.XPATH,'//*[@id="detail"]/div[1]/ul/li[5]')
                pl.click()
                time.sleep(2)
                if isElementExist('//*[@id="comm-curr-sku"]'):
                    try:
                        dqpl = browser.find_element(By.XPATH, '//*[@id="comm-curr-sku"]')
                        time.sleep(3)
                        dqpl.click()
                    except:
                        browser.close()
                        browser.switch_to.window(browser.window_handles[0])
                        continue
                else:
                    browser.close()
                    browser.switch_to.window(browser.window_handles[0])
                    continue

        time.sleep(2)
        try:
            qbpl = browser.find_element(By.XPATH,'//*[@id="comment"]/div[2]/div[2]/div[1]/ul/li[1]/a/em').text.strip()
        except:
            qbpl = ''
        try:
            st = browser.find_element(By.XPATH,'//*[@id="comment"]/div[2]/div[2]/div[1]/ul/li[2]/a').text.strip()
        except:
            st = ''
        try:
            spsd = browser.find_element(By.XPATH,'//*[@id="comment"]/div[2]/div[2]/div[1]/ul/li[3]/a/em').text.strip()
        except:
            spsd = ''
        try:
            zp = browser.find_element(By.XPATH,'//*[@id="comment"]/div[2]/div[2]/div[1]/ul/li[4]/a/em').text.strip()
        except:
            zp = ''
        try:
            hp = browser.find_element(By.XPATH,'//*[@id="comment"]/div[2]/div[2]/div[1]/ul/li[5]/a/em').text.strip()
        except:
            hp = ''
        try:
            cp = browser.find_element(By.XPATH,'//*[@id="comment"]/div[2]/div[2]/div[1]/ul/li[7]/a').text.strip()
        except:
            cp = ''
        f.write(
            f" {price},{res}, {qbpl}, {st}, {spsd}, {zp}, {hp}, {cp}\n")
        print(f" {price}, {res}, {qbpl}, {st}, {spsd}, {zp}, {hp}, {cp}")
        f.close()
        browser.close()
        browser.switch_to.window(browser.window_handles[0])


if __name__ == '__main__':
    # range(1,3) 取到 1，2
    for i in range(3,4):
        page = i*2-1
        url = f'https://search.jd.com/Search?keyword=%E6%99%BA%E8%83%BD%E6%89%8B%E8%A1%A8&pvid=ede7e656ea1f4d49a4a3ac2e5f1d48e4&page={page}&s=176&click=0'
        browser.get(url)
        #加载整个页面
        browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(3)
        print(i)
        try:
            get_onepage()
        except:
            continue
