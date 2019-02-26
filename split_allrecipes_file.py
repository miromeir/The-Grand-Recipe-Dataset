import os
import sys

def main():
    lines = []
    file_number = int(sys.argv[1])

    with open("allrecipes_recipes_cuisine_url.txt" , "r") as myfile:
        lines = myfile.readlines()

    chunk_size = int(len(lines) / file_number)
    for i in range(file_number):
        partfile = lines[0:chunk_size]
        with open("part_"+str(i)+".txt" , "a") as tmpfile:
            tmpfile.writelines(partfile)
        lines = lines[chunk_size:]

    if len(lines) > 0:
        with open("part_"+str(file_number)+".txt" , "a") as tmpfile:
            tmpfile.writelines(lines)
        

if __name__ == "__main__":
    main()
