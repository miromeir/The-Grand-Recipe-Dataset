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
        while not self.grid_pages.empty():
            grid_page = self.grid_pages.get()
            self.crawl_grid_for_recipes(grid_page)
            


    def crawl_grid_for_recipes(self, grid_page):
        print("crawling_grid_for_recepies")
        cuisine_name = grid_page[0]
        print("cuisine:"+cuisine_name)
        url = grid_page[1]
        print("url:"+url)
        self.driver3.get(url)
        time.sleep(2)
        grid = self.driver3.find_element_by_id("fixedGridSection")
        cards = grid.find_elements_by_class_name("fixed-recipe-card")



        while True:
            old_len = len(cards)
            #Scroll to bottom
            self.driver3.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            #Wait for grid to grow
            print("sleeping 3 seconds")
            time.sleep(3)
            grid = self.driver3.find_element_by_id("fixedGridSection")
            cards = grid.find_elements_by_class_name("fixed-recipe-card")
            if old_len == len(cards):
                break

        for card in cards:
            try:
                img = card.find_element_by_class_name("grid-card-image-container")
                link = img.find_element_by_tag_name("a").get_attribute("href")

                self.recipes.put((cuisine_name,link))
                self.writeRecipeToFile((cuisine_name,link))
            except Exception as e:
                print(e)
                pass

    def writeRecipeToFile(self, recipe):
        cuisine = recipe[0]
        url = recipe[1]
        with open("allrecipes_recipes_cuisine_url.txt", "a") as myfile:
            myfile.write(cuisine+","+url+"\n")
            

    def index_recipes(self):
        while not self.recipes.empty():
            try:
                recipe = self.recipes.get()
                cuisine_name = recipe[0]
                link = recipe[1]
                self.driver2.get(link)
                print(self.driver2.title)

                ingredients1 = self.driver2.find_element_by_id("lst_ingredients_1").find_elements_by_tag_name("li")
                ingredients2 = self.driver2.find_element_by_id("lst_ingredients_2").find_elements_by_tag_name("li")
            
                ingredients_element = ingredients1 + ingredients2
                ingredients = ""
                for ingredient in ingredients_element:
                    ingredients = ingredients + ingredient.text + "\n"
                
                recipe_title = self.driver2.title
                
                instructions_elements = self.driver2.find_elements_by_xpath("//li[@class='step']")
                instructions = ""
                for instruction in instructions_elements:
                    instructions = instructions + instruction.text +"\n\n"
                
                print("adding to database:"+recipe_title)
                self.add_recipe_to_database([("title",recipe_title),
                                        ("cuisine", cuisine_name),
                                        ("ingredients",ingredients),
                                        ("instructions",instructions)])

                    

            except Exception as e:
                print(e)
                pass

    def add_recipe_to_database(self,recipe):

        with open("allrecepies/"+recipe[0][1]+".txt", "a") as myfile:
            myfile.write("<recipe>"+"\n")
            for component in recipe:
                myfile.write("<"+component[0]+">"+"\n"+
                                            component[1]+"\n"+
                                        "</"+component[0]+">\n")
            myfile.write("</recipe>"+"\n")

    def __init__(self):

        self.recipes = queue.Queue()
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
        self.driver1 = webdriver.PhantomJS(service_args=['--load-images=no', '--disk-cache=true'], executable_path=os.path.abspath('./phantomjs'))
        self.driver3 = webdriver.PhantomJS(service_args=['--load-images=no', '--disk-cache=true'], executable_path=os.path.abspath('./phantomjs'))
        self.driver2 = webdriver.PhantomJS(service_args=['--load-images=no', '--disk-cache=true'], executable_path=os.path.abspath('./phantomjs'))
        
        self.crawl_for_grid_pages()
        self.crawl_grids()
        #self.index_recipes()


        # find_grids_thread = Thread(target = self.crawl_for_grid_pages)
        # find_grids_thread.start()

        # find_recipes_in_grids = Thread(target = self.crawl_grids)
        # find_recipes_in_grids.start()

        # process_recipe_thread = Thread(target = self.index_recipes)
        # process_recipe_thread.start()

        print("Program Ended")


if __name__ == '__main__':
    Crawler()
