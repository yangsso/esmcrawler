import sys
import os
from time import sleep
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select


class ESMCrawler:

    def __init__(self, id, pwd):
        self.driver = webdriver.Chrome('./chromedriver')
        self.id = id
        self.pwd = pwd

    def login(self):
        #로그인
        self.driver.implicitly_wait(3)
        self.driver.get('https://www.esmplus.com/Member/SignIn/LogOn')

        self.driver.find_element_by_id('rdoSiteSelect').click()
        self.driver.find_element_by_id('SiteId').send_keys(self.id)
        self.driver.find_element_by_id('SitePassword').send_keys(self.pwd)
        self.driver.find_element_by_id('btnSiteLogOn').click()

    def close_popup(self):
        if len(self.driver.window_handles) > 1:
            for i in range(1, len(self.driver.window_handles)):
                self.driver.switch_to.window(self.driver.window_handles[i])
                self.driver.close()

        self.driver.switch_to.window(self.driver.window_handles[0])

    def enroll_item(self):
        self.driver.get('https://www.esmplus.com/Sell/SingleGoods?menuCode=TDM395')

        #카테고리
        values = self.driver.find_elements_by_class_name('search_value')
        btns = self.driver.find_elements_by_class_name('search_submit')

        values[0].send_keys("팬츠")
        btns[0].click()
        sleep(3)
        res_list = self.driver.find_elements_by_class_name('keyword')
        f_len = len(res_list)
        res_list[0].click()

        sleep(3)
        values[1].send_keys("팬츠")
        values[1].send_keys(Keys.RETURN)
        sleep(3)
        res_list = self.driver.find_elements_by_class_name('keyword')
        s_len = len(res_list)
        res_list[f_len].click()

        sleep(3)
        values[2].send_keys("팬츠")
        values[2].send_keys(Keys.RETURN)
        sleep(3)
        res_list = self.driver.find_elements_by_class_name('keyword')
        res_list[f_len + s_len].click()

        #상품명
        sleep(2)
        self.driver.find_element_by_id('txtGoodsNameSearch').send_keys("TEST "+ str(datetime.utcnow())[0:10])
        self.driver.find_element_by_id('txtGoodsNamePrmt').send_keys("PRMT")

        #가격
        sleep(2)
        self.driver.find_element_by_id('txtGoodsPrice').send_keys("10000")
        self.driver.find_element_by_id('chkSellerDiscountIsUsed').click()
        sleep(1)
        self.driver.find_element_by_id('SYIStep3_SellerDiscount_DiscountAmt').send_keys('1000')

        #재고
        self.driver.find_element_by_id('chkGoodsCountUsed').click()
        sleep(1)
        self.driver.find_element_by_id('txtGoodsCountIAC').send_keys('100')
        self.driver.find_element_by_id('txtGoodsCountGMKT').send_keys('200')

        #to step2
        self.driver.find_element_by_class_name('button-step-next').click()
        sleep(1)

        #_____test이미지 업로드
        self.driver.find_element_by_class_name('reg_file').send_keys(os.getcwd() + '/test.jpg')
        sleep(2)

        #desc
        windows = self.driver.window_handles
        self.driver.find_element_by_id('btnNewDesc').click()
        popup_window = self.driver.window_handles[len(windows)]
        self.driver.switch_to.window(popup_window)

        for i in range(0,10):
            self.driver.find_element_by_class_name('slider-roll-next').click()
        sleep(2)
        self.driver.find_element_by_class_name('layer-close-button').click()

        self.driver.find_element_by_class_name('ee-contents').send_keys('testestsete')
        self.driver.find_element_by_id('btnSave').click()
        self.driver.find_element_by_class_name('ee-button-positive').click()
        self.driver.close()

        self.driver.switch_to.window(self.driver.window_handles[0])

        #템플릿
        select = Select(self.driver.find_element_by_id('ddlOfficialNotiTemplateList'))
        select.select_by_value('11370')

        #배송방법

        self.driver.find_element_by_id('rdoCommonDeliveryWayOPTSEL1').click()
        sleep(2)

        #배송비 탬플릿
        select = Select(self.driver.find_element_by_id('selBundleDeliveryTemp'))
        select.select_by_value('3214627')

        self.driver.find_element_by_class_name('button-step-next').click()
        self.driver.find_element_by_class_name('button-step-next').click()

        sleep(2)
        self.driver.find_element_by_class_name('is-active').click()
        sleep(2)
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.find_element_by_id('lbConfirmForGoodsImage').click()
        self.driver.find_element_by_id('lblConfirmForGoodsName').click()
        self.driver.find_element_by_id('lblConfirmForSellerDiscount').click()
        self.driver.find_element_by_id('lblConfirmForGoodsPrice').click()
        self.driver.find_element_by_id('btnConfirm').click()


if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("필요 arg 부족")
        exit()

    id = sys.argv[1]
    pwd = sys.argv[2]
    cralwer = ESMCrawler(id, pwd)
    try:
        cralwer.login()
    except:
        print("LOGIN FAIL")

    sleep(1)
    cralwer.close_popup()
    cralwer.enroll_item()
