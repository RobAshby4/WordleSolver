from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Firefox()

class Letter:
    state = "empty"
    character = ''
    def __init__(self, state, character):
        self.state = state
        self.character = character


class Board:
    rows = {
        1: [],
        2: [],
        3: [],
        4: [],
        5: [],
        6: [],
    }
    def __init__(self, board_elem):
        row_elems = board_elem.find_element(By.XPATH, "./child::*")
        i = 1
        for row in row_elems:
            print(i)
            i += 1
        

def get_current_board():
    global driver 
    global board_state
    board_div = driver.find_element(By.XPATH, "/html/body/div/div/div[4]/main/div[1]/div")
    return Board(board_div)
    print("TODO")

def main():
    global driver
    driver.get("https://www.nytimes.com/games/wordle/index.html")
    driver.find_element(By.XPATH, "/html/body/div/div/div/div/div/div[2]/button[2]").click()
    driver.find_element(By.XPATH, "/html/body/div/div/dialog/div/div/button").click()
    current_board = get_current_board()
    time.sleep(100)

if __name__ == "__main__":
    main()