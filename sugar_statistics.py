import os
from xml.etree import ElementTree
from functools import reduce


def getMgSugar(unit):
    Sugarg = {}
    Sugarg['Tablespoon'] = 10
    Sugarg['Cup'] = 160
    Sugarg['Pound'] = 453
    Sugarg['Teaspoon'] = 7.5
    Sugarg['Quart'] = Sugarg['Cup']*4
    Sugarg['Ounce'] = 28.5
    Sugarg[''] = 150
    try:
        value = Sugarg[unit]
        return value

    except Exception as e:
        return 0

def getAverage(cuisine, requested_ingredient):

    Dir = "Results/Recipes_TAGGED"
    filenames = os.listdir(Dir)
    amounts = []
    
    for filename in filenames:
        with open(Dir+"/"+filename, "r") as myFile :
            tree = ElementTree.parse(myFile)
            if cuisine.title() in tree.getroot().find("cuisine").text.title():
                
                for ingredient in (tree.getroot().find("ingredients").findall("ingredient")):
                    if ingredient.text == requested_ingredient:
                        
                        if not any(map((lambda x : x[0] == ingredient.attrib.get('unit',"")), amounts)):
                            amounts = amounts + [(ingredient.attrib.get('unit',""),[ingredient.attrib.get('amount',"1")])]
                        else:
                            for elem in amounts:
                                if elem[0] == ingredient.attrib.get('unit',""):
                                    if ingredient.attrib.get('amount',"") == "":
                                        elem[1].append(1)
                                    else:
                                        elem[1].append(ingredient.attrib.get('amount',""))
    result=[]
    
    for amount in amounts:
        #result.append((amount[0], list(map(float, amount[1])) ) )
        
        result.append((amount[0],  reduce(lambda x,y: x+y,   map( float , amount[1]) ) / len(amount[1])    ))

    return result
    
    
                        
                        
                        
                        
def main():
    Dir = "Results/Recipes_TAGGED"
    filenames = os.listdir(Dir)
    my_ingredient = "Onion"
    cuisines = []
    for filename in filenames:
        with open(Dir+"/"+filename, "r") as myFile :
            tree = ElementTree.parse(myFile)
            cuisine = tree.getroot().find("cuisine").text.strip().title()
            if not (cuisine in cuisines):
                cuisines.append(cuisine)
    
    for cuisine in cuisines:
        amounts = getAverage(cuisine, my_ingredient)
        total = 0
        for amount in amounts:
            total = total + getMgSugar(amount[0]) * amount[1] # total += weightInGrams * amount
        
        if len(list(filter(lambda x : getMgSugar(x[0]) > 0, amounts))) > 0:
            avg = total / len(list(filter(lambda x : getMgSugar(x[0]) > 0, amounts)))
        else:
            avg = 0
        

        print(cuisine+":"+ str(avg))

            

if __name__ == "__main__":
    main()