import time
import os
from xml.etree import ElementTree
from threading import Thread
import re
import json

word_list = []
with open("Wikidata_Keywords.json", 'r') as myfile:
    rows = json.load(myfile)
    for row in rows:
        word_list = word_list + [row['____Label']]


def amount_and_material(astring):
    
    units_of_measure = []
    with open("Units_of_Measurement.txt","r") as myFile:
        units_of_measure = myFile.readlines()
    

    amount_match = re.findall(r'[0-9]+[\\,/,\.]*[0-9]*', astring)
    amount = ""

    
    if(len(amount_match) > 0):
        
        amount_str = amount_match[0]
        if is_simpleFraction(amount_str):
            nom = amount_str[0:amount_str.index('/')]
            den = amount_str[amount_str.index('/')+1:]
            amount = str(float(nom)/float(den))
        else:
            amount = str(float(amount_str))
        
        astring = (astring[0:astring.index(amount_str)] + astring[(astring.index(amount_str)+len(amount_str)) :]).strip()

        for word in units_of_measure:
           
            if word.title() in astring.title():
                amount = amount + " " + word
                break
    
    ingredient_matches = []
    for word in word_list:
        if word.title() in astring.title():
            ingredient_matches = ingredient_matches + [word.title()]
    
    chosen_ingredient = ""
    if len(ingredient_matches) > 0:
        chosen_ingredient = max(ingredient_matches,key=len)

    
    return amount, chosen_ingredient

def is_simpleFraction(str):
    try:
        if str.index('/'):
            return True

    except Exception as e:
        return False
    
    
def main():
    Dir = 'Results/Recipes_UNTAGGED'
    files_list = os.listdir(Dir)
    filecount = len(files_list)
    for filename in files_list:
        try:
            with open(Dir+"/"+filename, "r") as myfile:
                tree = ElementTree.parse(myfile)
                ingredients_node = tree.find(".//ingredients")
                
                ingredients = ingredients_node.text.split("\n")[1:-3]
                ingredients_node.text = ""
                for ingredient in ingredients:
                        amount, material = amount_and_material(ingredient)
                        if len(material) > 0:
                            
                            newtag = ElementTree.SubElement(ingredients_node, "ingredient")
                            newtag.text = material
                            newtag.attrib['amount'] = amount
                            tree.write("Results/Recipes_TAGGED/"+filename)
        except Exception as e:
            print(e)
            pass

if __name__ == '__main__':
    main()