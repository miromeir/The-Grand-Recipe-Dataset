import time
import os
from xml.etree import ElementTree
from threading import Thread
import re
import json

def main():
    Dir = 'recepies'   
    files_list = os.listdir(Dir)
    filecount = len(files_list)
    for filename in files_list:
        try:
            with open(Dir+"/"+filename, "r") as myfile:
                tree = ElementTree.parse(myfile)
                details_node = tree.find(".//details")
                details = details_node.text.split('\n')
                cuisine = ""
                for detail in details:
                    if "CUISINE:" in detail:
                        cuisine = detail[detail.index("CUISINE:") + len("CUISINE") + 1:].strip()
                        print(cuisine)
                
                if len(cuisine) > 0:
                    recipe_node = tree.find(".")
                    newtag = ElementTree.SubElement(recipe_node , "cuisine")
                    newtag.text = cuisine
                
                    tree.write("output_iheartrecipes/"+filename)

        except Exception as e:
            print(e)
            pass

if __name__ ==  "__main__":
    main()