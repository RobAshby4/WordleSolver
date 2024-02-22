from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()

class Letter:
    state = "empty"
    character = ''

    def __init__(self, state, character):
        self.state = state
        self.character = character

    def set_state(state):
        self.state = state

    def set_character(character):
        self.character = character

class Row:
    word = None
    letters = []
    def __init__(self, row):
        row_word = ""
        elements = row.find_elements(By.XPATH, './div/*')
        for element in elements:
            row_word = row_word + element.text
            self.letters.append(Letter(element.get_attribute('data-state'), element.text))
        self.word = row_word

class Board:
    rows = {
        1: None,
        2: None,
        3: None,
        4: None,
        5: None,
        6: None,
    }

    def __init__(self, board_elem, guess_num):
        for i in range (1, 7):
            next_row = driver.find_element(By.XPATH, '//div[@aria-label="Row {}"]'.format(i))
            self.rows[i] = Row(next_row)
            print(str(i))
            print(self.rows[i].word)


def get_current_board():
    global driver 
    global board_state
    board_div = driver.find_element(By.XPATH, '//*[@id="wordle-app-game"]/div[1]/div')
    return Board(board_div, 1)
    print("TODO")

def main():
    global driver
    driver.get("https://www.nytimes.com/games/wordle/index.html")
    driver.find_element(By.XPATH, "/html/body/div/div/div/div/div/div[2]/button[2]").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "/html/body/div/div/dialog/div/div/button").click()
    body = driver.find_element(By.XPATH, "html/body")
    time.sleep(1)
    body.send_keys("arise", Keys.RETURN)
    time.sleep(3)
    body.send_keys("match", Keys.RETURN)
    current_board = get_current_board()
    time.sleep(100)

if __name__ == "__main__":
    main()
