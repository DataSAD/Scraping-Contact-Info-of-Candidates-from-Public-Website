from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import openpyxl


cat_dict = [{'Name': [], 'Phone': [], 'Website': [], 'email': [], 'Facebook': [], 'Twitter': [], 'Instagram': []},
            {'Name': [], 'Phone': [], 'Website': [], 'email': [], 'Facebook': [], 'Twitter': [], 'Instagram': []},
            {'Name': [], 'Phone': [], 'Website': [], 'email': [], 'Facebook': [], 'Twitter': [], 'Instagram': []},
            {'Name': [], 'Phone': [], 'Website': [], 'email': [], 'Facebook': [], 'Twitter': [], 'Instagram': []},
            {'Name': [], 'Phone': [], 'Website': [], 'email': [], 'Facebook': [], 'Twitter': [], 'Instagram': []}]


category = {1: 'Presidencia de la República',
            2: 'Senaduría Federal Mayoría Relativa',
            3: 'Senaduría Federal Representación Proporcional',
            4: 'Diputación Federal Mayoría Relativa',
            5: 'Diputación Federal Representación Proporcional'}


options = webdriver.ChromeOptions()
options.add_argument('start-maximized')
options.add_experimental_option('detach', True)
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(15)
actions = ActionChains(driver)


def select_category(category_no):
    driver.get('https://candidaturas.ine.mx/')

    select_category_field = driver.find_element(By.ID, 'busqueda-form_tipoCandidatura')
    actions.move_to_element(select_category_field).perform()
    select_category_field.click()

    category_button = driver.find_element(By.XPATH, f'//div[text()="{category_no}"]')
    actions.move_to_element(category_button).perform()
    category_button.click()

    consultar_button = driver.find_element(By.XPATH, '//span[text()="Consultar"]')
    actions.move_to_element(consultar_button).perform()
    consultar_button.click()


def get_links(cat_no):
    candidates = []
    container = driver.find_element(By.CSS_SELECTOR, 'tbody[class="ant-table-tbody"]')
    links = container.find_elements(By.CSS_SELECTOR, 'a')

    if cat_no == 1:
        for link in links:
            candidates.append(link.get_attribute('href'))
    else:
        for i, link in enumerate(links):
            if i % 2 == 0:
                candidates.append(link.get_attribute('href'))

    return candidates


def get_page_count():
    return int(driver.find_element(By.XPATH, '//li[@title="Página siguiente"]/preceding-sibling::*[1]').get_attribute('title'))


for category_no in range(1, 6):

    while True:
        try:
            select_category(category[category_no])
            break
        except:
            pass

    pages = get_page_count()

    for page in range(pages):

        for n in range(page):
            next_button = driver.find_element(By.XPATH, '//li[@title="Página siguiente"]/button')
            actions.move_to_element(next_button).perform()
            next_button.click()

        candidate_links = get_links(category_no)

        for i, link in enumerate(candidate_links):
            print(f'category: {category_no}        page: {page + 1}        candidate: {i+1}')

            driver.get(link)

            Name = driver.find_element(By.CSS_SELECTOR, 'div[data-det="nombreCandidato"]').text
            cat_dict[category_no-1]['Name'].append(Name)
            Phone = driver.find_element(By.CSS_SELECTOR, 'span[data-det="telefonoPublico"]').text
            cat_dict[category_no-1]['Phone'].append(Phone)
            Website = driver.find_element(By.XPATH, '//div[text()="Página web: "]/following-sibling::div/span').text
            cat_dict[category_no-1]['Website'].append(Website)
            email = driver.find_element(By.XPATH, '//div[text()="Correo electrónico público: "]/following-sibling::div/span').text
            cat_dict[category_no-1]['email'].append(email)
            try:
                Facebook = driver.find_element(By.XPATH, '//span[@aria-label="facebook"]/parent::a').get_attribute('href')
                cat_dict[category_no-1]['Facebook'].append(Facebook)
            except:
                cat_dict[category_no-1]['Facebook'].append('No Info')
            try:
                Twitter = driver.find_element(By.XPATH, '//span[@aria-label="twitter"]/parent::a').get_attribute('href')
                cat_dict[category_no-1]['Twitter'].append(Twitter)
            except:
                cat_dict[category_no-1]['Twitter'].append('No Info')
            try:
                Instagram = driver.find_element(By.XPATH, '//span[@aria-label="instagram"]/parent::a').get_attribute('href')
                cat_dict[category_no-1]['Instagram'].append(Instagram)
            except:
                cat_dict[category_no-1]['Instagram'].append('No Info')

        while True:
            try:
                select_category(category[category_no])
                break
            except:
                pass
       

    df = pd.DataFrame(cat_dict[category_no-1])
    df.to_excel(f'{category_no}.xlsx')






