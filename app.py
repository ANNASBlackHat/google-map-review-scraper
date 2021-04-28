from selenium import webdriver
import time
import json
import re


def extract_url(text):
    s = re.search('(?P<url>https?://[^\s\)"]+)', text)
    if s != None:
        return s.group("url")
    else:
        return text


def get_date(section):
    dates = section.find_elements_by_class_name('section-review-publish-date')
    if len(dates) > 0 :
        return dates[0].text

    dates = section.find_elements_by_class_name('section-review-publish-date-and-source')
    if len(dates) > 0:
        return dates[0].text
    return ''


def get_rating(section):
    stars = section.find_elements_by_class_name('section-review-stars')
    if len(stars) > 0:
        return stars[0].get_attribute('aria-label')

    stars = section.find_elements_by_class_name('section-review-numerical-rating')
    if len(stars) > 0:
        return stars[0].text
    return ''


print('init driver...')
firefox_options = webdriver.FirefoxOptions()
driver = webdriver.Remote(
    command_executor='http://localhost:4444/wd/hub',
    options=firefox_options
)

result = []
try:
    print('opening website...')
    driver.get("https://www.google.co.id/maps/place/Grand+Inna+Malioboro/@-7.7845335,110.3904599,14z/data=!4m10!1m2!2m1!1sHotels!3m6!1s0x2e7a582f54bd487b:0xdfb5f572cc5945fc!5m2!4m1!1i2!9m1!1b1")

    time.sleep(15)

    btn_expands = driver.find_elements_by_class_name('section-expand-review')
    print('expands size --> ', len(btn_expands))
    for btn in btn_expands:
        btn.click()

    for i in range(0, 50):
        scrollable_div = driver.find_element_by_css_selector('div.section-layout.section-scrollbox')
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
        time.sleep(5)

        btn_expands = driver.find_elements_by_class_name('section-expand-review')
        print(i+1, '. expands size --> ', len(btn_expands))
        for btn in btn_expands:
            btn.click()

        # usernames = driver.find_elements_by_class_name('section-review-title')
        # print('usernames --> ', len(usernames))
        #
        # reviews = driver.find_elements_by_class_name('section-review-text')
        # print('total review now -> ',len(reviews))

    time.sleep(5)

    # usernames = driver.find_elements_by_class_name('section-review-title')
    # print('usernames --> ', len(usernames))
    #
    # stars = driver.find_elements_by_class_name('section-review-stars')
    # print('total stars now -> ',len(stars))
    # # for star in stars:
    # #     print(star.get_attribute('aria-label'))
    #
    # dates = driver.find_elements_by_class_name('section-review-publish-date')
    # print('total dates -> ',len(dates))
    #
    # reviews = driver.find_elements_by_class_name('section-review-text')
    # print('total review -> ',len(reviews))
    #
    # for i, review in enumerate(reviews):
    #     result.append({
    #     'username': usernames[i].text if len(usernames) > i else '',
    #     'star': stars[i].get_attribute('aria-label') if len(stars) > i else '',
    #     'date': dates[i].text if len(dates) > i else '',
    #     'review': review.text})

    review_sections = driver.find_elements_by_class_name('section-review')
    print('total review: ', len(review_sections))
    for section in review_sections:
        username = section.find_element_by_class_name('section-review-title').text
        date = get_date(section)
        review = section.find_element_by_class_name('section-review-text').text
        star = get_rating(section)
        response = section.find_elements_by_class_name('section-review-owner-response')
        photoes = section.find_elements_by_class_name('section-review-photos')

        data = {'username': username, 'star': star, 'date': date, 'review': review}

        if len(response) > 0:
            data['response'] = response[0].find_element_by_class_name('section-review-text').text

        if len(photoes) > 0:
            urls = []
            for photo in photoes:
                #section-review-photo
                url = photo.find_element_by_class_name('section-review-photo').get_attribute('style')
                urls.append(extract_url(url))
            data['photoes'] = urls


        print(username, star, date);
        result.append(data)

    time.sleep(3)
finally:
    # driver.close()
    driver.quit()


# print(result)
with open('output.txt', 'w') as f:
    json.dump(result, f)
