import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class WordleGame:
    def __init__(self):
        # init driver and dictionary
        self.driver = webdriver.Chrome()
        self.words = list(filter(lambda x: len(x) == 5, open('words.txt', 'r').read().split('\n')))
        if self.words == None:
            print("couldn't find dictionary file 'words.txt', exiting...")
            exit(1)

        # load wordle website and get to the game
        self.driver.get("https://www.nytimes.com/games/wordle/index.html")
        self.driver.find_element(By.XPATH, "/html/body/div/div/div/div/div/div[2]/button[2]").click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, "/html/body/div/div/dialog/div/div/button").click()
        self.body = self.driver.find_element(By.XPATH, "html/body")
        time.sleep(1)

    def make_guess(self, word):


    def make_guess_rand(self):
        make_guess()

    def get_last_line(self):


def main():
    game = WordleGame()

if __name__ == "__main__":
    main()
