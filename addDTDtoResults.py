import time
import os
from xml.etree import ElementTree
from threading import Thread
import re
import json
import sys
import os

def main():
    Dir = sys.argv[1]
    filenames = os.listdir(Dir)
    for filename in filenames:
        with open(Dir+"/"+filename,"r+") as myFile:
            originalcontent = myFile.read()
            myFile.seek(0)
            myFile.write("<?xml version = "1.0" ?>")
            myFile.write("\n")
            myFile.write("<!DOCTYPE recipe [<!ELEMENT recipe ((title?,details?,ingredients, instructions?,cuisine) | (title?,cuisine,details?,ingredients, instructions?))><!ELEMENT title (#PCDATA)><!ELEMENT cuisine (#PCDATA)><!ELEMENT ingredients (#PCDATA)><!ELEMENT instructions (#PCDATA)><!ELEMENT details (#PCDATA)>]>")
            myFile.write("\n")
            myFile.write(originalcontent)
            
    

    
if __name__ == '__main__':
    main()