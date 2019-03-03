#!/usr/bin/env python
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import queue
from threading import Thread

class Crawler():
    def crawl_for_recipes(self):
        page_idx = 1
        while(page_idx <= 57):
            self.crawl_page_for_recipes("https://www.ihearteating.com/recipe-index-2/?fwp_paged="+str(page_idx))
            page_idx = page_idx+1
    def crawl_page_for_recipes(self, url):
        print("crawling_page_for_recepies")
        self.driver1.get(url)
        mydivs = self.driver1.find_element_by_class_name("site-inner").find_elements_by_tag_name("article")

        for elem in mydivs:
            try:
                link_tag = elem.find_element_by_tag_name("a")
                link_href = link_tag.get_attribute("href")
                self.to_visit_list.put(link_href)
            except Exception as e:
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
        self.driver1 = webdriver.PhantomJS(executable_path=os.path.abspath('/home/miro/Crawler/phantomjs'))
        self.driver2 = webdriver.PhantomJS(executable_path=os.path.abspath('/home/miro/Crawler/phantomjs'))
        index_thread = Thread(target = self.crawl_for_recipes)
        index_thread.start()

        process_recipe_thread = Thread(target = self.index_recipes)
        process_recipe_thread.start()

        index_thread.join()


        print("Program Ended")


if __name__ == '__main__':
    Crawler()
