from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import json
import sys
import datetime


class Game:
    def __init__(self, gameTitle, gameCode):
        self.gameTitle = gameTitle
        self.gameCode = gameCode
        self.gameUrl = "https://ec.nintendo.com/AU/en/titles/" + gameCode

    # class = status-bottom
    def checkPrice(self, driver):
        driver.get(self.gameUrl)
        timeout = 3
        try:
            element = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.CLASS_NAME, "o_p-product-detail__price--price")))
            if not element.text:        # No Content was found in element, shouldn't happen though
                raise ValueError
            self.price = element.text
        except TimeoutException:        # Page took too long to load, usually because page doesn't exist
            self.price = "Couldn't find game"
        except ValueError:
            print("Couldn't find price, trying again...")
            self.checkPrice(driver)

    def checkIfSale(self, driver):
        driver.get(self.gameUrl)
        try:
            element = WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.CLASS_NAME, "o_c-message ")))
            if element.text:
                self.sale = element.text

        except TimeoutException:
            self.sale = "No Sale"


print(datetime.date.today())
gameJsons = json.loads(open('nintendoGames.json').read())

options = webdriver.FirefoxOptions()
options.add_argument("-headless")
driver = webdriver.Firefox(options=options, executable_path="C:\\firefox_driver\geckodriver.exe")

games = []
for game in gameJsons:
    games.append(Game(game["title"], game["code"]))

for game in games:
    game.checkPrice(driver)
    game.checkIfSale(driver)
    print(game.gameTitle + ": " + game.price + " " + game.sale)

driver.quit()

