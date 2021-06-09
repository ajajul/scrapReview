from selenium import webdriver
import time
from selenium.webdriver.firefox.options import Options

options = Options()
options.add_argument("--headless")


def fetchReviews():
    i = 0
    driver = webdriver.Firefox(executable_path='./geckodriver', options=options)
    driver.get('https://www.google.com/search?q=bmw+of+austin#lrd=0x8644cd1fdca503e1:0x49fed3597ce3a823,1,,,')
    time.sleep(5)
    data = []
    stop_scrap = False
    while True:
        review_dialog_list = driver.find_elements_by_class_name("review-dialog-list")[0]
        review_outer_block = review_dialog_list.find_elements_by_class_name("gws-localreviews__general-reviews-block")[i]
        for review in review_outer_block.find_elements_by_class_name("gws-localreviews__google-review"):
            if 'year' in review.find_elements_by_class_name("PuaHbe")[0].get_attribute("innerText"):
                stop_scrap = True
                break
            review_text = ""
            full_text = review.find_elements_by_class_name("review-full-text")
            if len(full_text) > 0:
                review_text = full_text[0].get_attribute("innerText")
            else:
                review_text = review.find_elements_by_class_name("Jtu6Td")[0].get_attribute("innerText")
            data.append({
                "review_time": review.find_elements_by_class_name("PuaHbe")[0].get_attribute("innerText"),
                "reviewer_name":  review.find_elements_by_class_name("TSUbDb")[0].get_attribute("innerText"),
                "rating": int(review.find_elements_by_class_name("Fam1ne")[0].get_attribute("aria-label")[6:7]),
                "review_text": review_text
            })
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", review_dialog_list)
        time.sleep(5)
        if stop_scrap:
            break
        i += 1
    driver.quit()
    return data