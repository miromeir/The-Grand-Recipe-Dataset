#!/usr/bin/env python
import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import queue
from threading import Thread

class Crawler():
    def crawl_for_grid_pages(self):
        self.driver1.get("https://www.allrecipes.com/recipes/86/world-cuisine/?internalSource=top%20hubs&referringContentType=Homepage")
        slider = self.driver1.find_element_by_id("insideScroll")
        all_cuisins = slider.find_elements_by_tag_name("li")
        
        #get all types of cuisins from main page:
        for li in all_cuisins:
            link = li.find_element_by_tag_name("a").get_attribute("href")
            cuisine_name = li.find_element_by_tag_name("span").text.replace("Recipes","").strip() #Remove the word 'Recipes'
            self.grid_pages.put((cuisine_name,link))
            
    def crawl_grids(self):
        while True:
            if not self.grid_pages.empty():
                grid_page_url = self.grid_pages.get()
                self.crawl_grid_for_recipes(self, grid_page_url)
                


    def crawl_grid_for_recipes(self, url):
        print("crawling_grid_for_recepies")
        self.driver1.get(url)

        grid = self.driver1.find_element_by_id("fixedGridSection")
        cards = grid.find_elements_by_class_name("fixed-recipe-card")
        
        
        
        while True:
            old_len = len(cards)
            #Scroll to bottom
            self.driver1.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            #Wait for grid to grow
            time.sleep(5)
            grid = self.driver1.find_element_by_id("fixedGridSection")
            cards = grid.find_elements_by_class_name("fixed-recipe-card")
            if old_len == len(cards):
                break
        
        for card in cards:
            try:
                img = card.find_elements_by_class_name("grid-card-image-container")
                link_href = link_tag.get_attribute("href")
                
                self.to_visit_list.put(link_href)
            except Exception as e:
                print(e)
                pass

    def index_recipes(self):
        while True:
            try:
                if not self.to_visit_list.empty():

                    link = self.to_visit_list.get()
                    self.driver2.get(link)
                    print(self.driver2.current_url)
                    recipe = self.driver2.find_element_by_xpath("//div[@class='wprm-recipe-container']")
                    recipe_ihe = recipe.find_element_by_xpath("div[@class='wprm-recipe wprm-recipe-ihe']")
                    recipe_header = recipe_ihe.find_element_by_xpath("div[@class='wprm-entry-header']")
                    recipe_content = recipe_ihe.find_element_by_xpath("div[@class='wprm-entry-content']")
                    recipe_title = recipe_header.find_element_by_xpath("h2[@class='wprm-recipe-name']")
                    recipe_details = recipe_header.find_element_by_xpath("div[@class='wprm-recipe-details-container']")
                    recipe_ingredients_container = recipe_content.find_element_by_xpath("div[@class='wprm-recipe-ingredients-container']")
                    recipe_ingredients = recipe_ingredients_container.find_element_by_xpath("div[@class='wprm-recipe-ingredient-group']")
                    recipe_instructions_container = recipe_content.find_element_by_xpath("div[@class='wprm-recipe-instructions-container']")
                    recipe_instructions = recipe_instructions_container.find_element_by_xpath("div[@class='wprm-recipe-instruction-group']")

                    self.add_recipe_to_database([("title",recipe_title.text),
                                            ("details",recipe_details.text),
                                            ("ingredients",recipe_ingredients.text),
                                            ("instructions",recipe_instructions.text)])

                    print(recipe_title.text)

            except Exception as e:
                print(e)
                pass

    def add_recipe_to_database(self,recipe):

        with open("recepies/"+recipe[0][1], "a") as myfile:
            myfile.write("<recipe>"+"\n")
            for component in recipe:
                myfile.write("<"+component[0]+">"+"\n"+
                                            component[1]+"\n"+
                                        "</"+component[0]+">\n")
            myfile.write("</recipe>"+"\n")

    def __init__(self):

        self.to_visit_list = queue.Queue()
        self.grid_pages = queue.Queue()
        self.outputFile = open("output.txt", "a")
        
        options = Options()
        options.headless = True

        # firefox_options.add_argument("--headless")
        # #chrome_options.binary_location = '/Applications/Google Chrome   Canary.app/Contents/MacOS/Google Chrome Canary'`
        # firefox_options.add_argument('--ignore-certificate-errors')
        # firefox_options.add_argument("--test-type")
        # firefox_options.add_argument('--no-proxy-server')
        # firefox_options.add_argument("--proxy-server='direct://'")
        # firefox_options.add_argument("--proxy-bypass-list=*")
        #caps = DesiredCapabilities().CHROME
        #caps["pageLoadStrategy"] = "eager"  #  complete
        self.driver1 = webdriver.PhantomJS(executable_path=os.path.abspath('./phantomjs'))
        self.driver2 = webdriver.PhantomJS(executable_path=os.path.abspath('./phantomjs'))
        find_grids_thread = Thread(target = self.crawl_for_grid_pages)
        find_grids_thread.start()

        process_recipe_thread = Thread(target = self.index_recipes)
        process_recipe_thread.start()

        index_thread.join()


        print("Program Ended")


if __name__ == '__main__':
    Crawler()
