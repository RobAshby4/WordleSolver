import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from PyDictionary import PyDictionary
from dataclasses import dataclass


words = list(filter(lambda x: len(x) == 5, open('words.txt', 'r').read().split('\n')))
driver = webdriver.Chrome()
dictionary=PyDictionary()

## TODO: refactor into board
possibilities = {
    1:  list('abcdefghijklmnopqrstuvwxyz'),
    2:  list('abcdefghijklmnopqrstuvwxyz'),
    3:  list('abcdefghijklmnopqrstuvwxyz'),
    4:  list('abcdefghijklmnopqrstuvwxyz'),
    5:  list('abcdefghijklmnopqrstuvwxyz'),
}
## TODO: refactor into board
sticky_chars = {
    1: "",
    2: "",
    3: "",
    4: "",
    5: "",
}
must_contain = []
body = None

class Letter:
    state = 'empty'
    character = ''

    def __init__(self, state, character):
        self.state = state
        self.character = character

    def set_state(self, state):
        self.state = state

    def set_character(self, character):
        self.character = character

class Row:
    def __init__(self, row):
        row_word = ""
        elements = row.find_elements(By.XPATH, './div/*')
        self.letters = []
        for element in elements:
            row_word = row_word + element.text
            elem_state = element.get_attribute('data-state')
            self.letters.append(Letter(elem_state, element.text))
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

def make_rand_guess():
    global driver
    global words
    global body
    random.shuffle(words)
    body.send_keys(words[0])
    time.sleep(1)
    body.send_keys(Keys.RETURN)
    time.sleep(3)
     
def make_guess(word):
    global driver
    global body
    body.send_keys(word)
    time.sleep(1)
    body.send_keys(Keys.RETURN)
    time.sleep(3)

def calc_next_guess():
    global possibilities
    board = get_current_board()
    for i in range(1, 7):
        row = board.rows[i]
        if not row.letters[0].state == 'empty':
            for j in range(1,6):
                l = row.letters[j - 1]
                if l.state == 'absent':
                    delete_char(l.character)
                if l.state == 'present':
                    delete_char_in(j, l.character)
                if l.state == 'correct':
                    add_sticky_char(j, l.character)
    apply_word_filter()
    return get_rand_word()

def add_sticky_char(position, char):
    global sticky_chars
    global possibilities
    sticky_chars[position] = char
    possibilities[position] = []

def get_rand_word():
    global words
    random.shuffle(words)
    return words[0]

def apply_word_filter():
    global possibilities
    global words 
    global must_contain
    for i in range(1, 6):
        if not sticky_chars[i] == "":
            possibilities[i].insert(0, str.lower(sticky_chars[i]))
        words = list(filter(lambda x: filter_place(i, x, possibilities[i]), words))
    for c in must_contain:
        words = list(filter(lambda x: c in x, words))

def filter_place(place, word, chars):
    if word[place - 1] not in chars:
        return False
    return True

def delete_char(char):
    global possibilities
    global sticky_chars
    char = str.lower(char)
    for i in range(1, 6):
        if char in possibilities[i]:
            possibilities[i].remove(char)

def delete_char_in(position, char):
    global possibilities
    global sticky_chars
    global must_contain
    char = str.lower(char)
    must_contain.append(char)
    if char in possibilities[position]:
        possibilities[position].remove(char)

def get_current_board():
    global driver 
    global board_state
    board_div = driver.find_element(By.XPATH, '//*[@id="wordle-app-game"]/div[1]/div')
    return Board(board_div, 1)

def main():
    global driver
    global body
    # navigate to game
    driver.get("https://www.nytimes.com/games/wordle/index.html")
    driver.find_element(By.XPATH, "/html/body/div/div/div/div/div/div[2]/button[2]").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "/html/body/div/div/dialog/div/div/button").click()
    body = driver.find_element(By.XPATH, "html/body")
    time.sleep(1)
    # loaded into game at this point
    make_rand_guess()
    next = calc_next_guess()
    make_guess(next)
    next = calc_next_guess()
    make_guess(next)
    next = calc_next_guess()
    make_guess(next)
    next = calc_next_guess()
    make_guess(next)
    next = calc_next_guess()
    make_guess(next)

    time.sleep(100)

if __name__ == "__main__":
    main()
