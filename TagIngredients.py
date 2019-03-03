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
    
    units_of_measure = [" Meter ",
    "Millimeter",
    "Centimeter",
    "Decimeter",
    "Kilometer",
    "Astronomical Unit",
    "Light Year",
    "Parsec",
    "Inch",
    "Foot",
    "Yard",
    "Mile",
    "Nautical Mile",
    "Square meter",
    "Acre",
    "Are",
    "Hectare",
    "Square inches",
    "Square feet",
    "Square yards",
    "Square miles",
    "Cubic meter",
    "Liter",
    "Milliliter",
    "Centiliter",
    "Deciliter",
    "Hectoliter",
    "Cubic Inch",
    "Cubic Foot",
    "Cubic Yard",
    "Acre-Foot",
    "Teaspoon",
    "Tablespoon",
    "Fluid ounce",
    "Cup",
    "Gill",
    "Pint",
    "Quart",
    "Gallon",
    "Radian",
    "Degree",
    "Steradian",
    "Second",
    "Minute",
    "Hour",
    "Day",
    "Year",
    "Hertz",
    "Angular Frequency",
    "Decibel",
    "Kilogram meters per second",
    "Miles per hour",
    "Meters per second",
    "Gravity Imperial",
    "Gravity Metric",
    "Feet per second",
    "Grams",
    "Kilogram",
    "Grain",
    "Dram",
    "Ounce",
    "Pound",
    "Hundredweight",
    "Ton",
    "Tonne",
    "Slug",
    "Density",
    "Newton",
    "Kilopond",
    "Pond",
    "Newton meter",
    "Joule",
    "Watt",
    "Kilowatt",
    "Horsepower",
    "Pascal",
    "Bar",
    "Pounds per square inch",
    "Kelvin",
    "Centigrade",
    "Calorie",
    "Fahrenheit",
    "Candela",
    "Candela per square metre",
    "Lumen",
    "Lux",
    "Lumen Seconds",
    "Diopter",
    "Ampere",
    "Coulomb",
    "Volt",
    "Ohm",
    "Farad",
    "Siemens",
    "Henry",
    "Weber",
    "Tesla",
    "Becquerel",
    "Mole",
    "Paper Bale",
    "Dozen",
    "mm ",
    "cm ",
    "dm ",
    "km ",
    "AE ",
    "lj ",
    "pc ",
    "in or ",
    "ft ",
    "yd ",
    "mi ",
    "sm ",
    "sqm or m2 ",
    "acre ",
    "a or ares ",
    "ha ",
    "in2 ",
    "ft2 ",
    "yd2 ",
    "mi2 ",
    "m3 ",
    "ml ",
    "l ",
    "cl ",
    "dl ",
    "hl ",
    "cu in or in3 ",
    "cu ft or ft3 ",
    "cu yd or yd3 ",
    "acre ft ",
    "tsp ",
    "tbsp ",
    "fl oz or oz. fl ",
    "cup ",
    "gill ",
    "pt or p ",
    "qt ",
    "gal ",
    "rad ",
    "deg ",
    "sr ",
    "s ",
    "min ",
    "h ",
    "d ",
    "a ",
    "Hz ",
    "dB ",
    "kg m/s ",
    "mph ",
    "m/s or kph ",
    "ft/s2 ",
    "m/s2 ",
    "ft/s ",
    "g ",
    "kg ",
    "gr ",
    "dr ",
    "oz ",
    "lb ",
    "cwt ",
    "ton ",
    "t ",
    "slug ",
    "kg/m3 ",
    "N ",
    "kp ",
    "p ",
    "J ",
    "w ",
    "kw ",
    "hp ",
    "Pa ",
    "bar ",
    "psi or lbf/in2 ",
    "K ",
    "C ",
    "Cal or kcal / cal ",
    "F ",
    "cd ",
    "cd/m2 ",
    "lm ",
    "lx ",
    "ls ",
    "dpt ",
    "A / Amps ",
    "C ",
    "V ",
    "S ",
    "H ",
    "Wb ",
    "(T) ",
    "Bq ",
    "mol ",
    "ream ",
    "dz or doz "]

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