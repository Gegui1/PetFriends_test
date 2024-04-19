import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Chrome()
    driver.get('https://petfriends.skillfactory.ru/login')
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


def test_show_all_pets(driver):
    driver.find_element(By.ID, 'email').send_keys('ooo@mail.ru')
    driver.find_element(By.ID, 'pass').send_keys('12345')
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.TAG_NAME, 'h1')))
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    driver.find_element(By.CSS_SELECTOR, 'li.nav-item > a.nav-link[href="/my_pets"]').click()

    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div#all_my_pets > table')))
    images = driver.find_elements(By.CSS_SELECTOR, 'div#all_my_pets > table > tbody > tr > th > img')
    names = driver.find_elements(By.CSS_SELECTOR, 'div#all_my_pets > table > tbody > tr > td')
    breeds = driver.find_elements(By.CSS_SELECTOR, 'div#all_my_pets > table > tbody > tr > td:nth-of-type(2)')
    ages = driver.find_elements(By.CSS_SELECTOR, 'div#all_my_pets > table > tbody > tr > td:nth-of-type(3)')

    images_count = 0
    list_names = []
    pets_count = driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text.split('\n')[1].split(': ')[1]
    print(f'количество питомцев в статистике', pets_count)

    for i in range(len(pets_count)):
        list_names.append(names[i].text)
        if images[i].get_attribute('src') != '':
            images_count += 1
        else:
            images_count += 0
        assert names[i].text != ''
        assert breeds[i].text != ''
        assert ages[i].text != ''
        print(images_count)
    if len(pets_count) == 0:
        print("No pets")
    else:
        assert images_count >= len(pets_count) / 2

    # Проверяем, что у питомцев разные имена
    set_name = set(list_names)
    assert len(set_name) == len(list_names)
