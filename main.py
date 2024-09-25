from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

def parse(p : int = 1):
    p = str(p)
    res = []
    # Настройки для использования Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Запуск в фоновом режиме
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # Создаем экземпляр сервиса ChromeDriver
    service = Service()
    # Инициализируем драйвер
    driver = webdriver.Chrome(service=service, options=chrome_options)
    try:
        # Переход на страницу
        driver.get(f'https://www.wildberries.ru/catalog/transportnye-sredstva/mototekxnika?page={p}')
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".product-card"))
            )
        except:
            return []
        # Получение всех элементов 
        cars = driver.find_elements(By.CSS_SELECTOR, '.product-card')  # Проверьте корректность селектора
        # проходимся по всем предложениям
        for car in cars:
            buf = []
            buf.append(car.find_element(By.CSS_SELECTOR, '.product-card__name').text)
            buf.append(car.find_element(By.CSS_SELECTOR, '.price').text)
            buf.append(car.find_element(By.CSS_SELECTOR, '.btn-text').text)
            buf.append(car.find_element(By.CSS_SELECTOR, ".product-card__link").get_attribute("href").split("/")[-2])
            res.append(buf)
    finally:
        driver.quit()  # Закрываем браузер
    return res

def main():
    result = []
    n = 1
    while True:
        buf = parse(n)
        if not buf:
            break
        result+=buf  # Добавляем все товары на странице
        n += 1
    # Открываем файл с указанием кодировки utf-8
    with open("data.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(result)
    
if __name__ == "__main__":
    main()