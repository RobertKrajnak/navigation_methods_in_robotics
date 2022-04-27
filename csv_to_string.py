import csv
import numpy as np
NumOfDice = 25
grid = []

with open("new_file.csv") as csvfile:
    reader = csv.reader(csvfile) # change contents to floats

    for row in reader: # each row is a list
        pole = []
        for number in row:
            pole.append(int(number))
        grid.append(pole)

print(grid)
print("grid type:",type(grid))

listToStr = '-'.join([str(elem) for elem in grid])

print(listToStr)
print("listToStr type:",type(listToStr))

listt = listToStr.split("-")
strToList = []

for i in listt:
    strToList.append(list(map(int, i[1:-1].split(", "))))

print(strToList)
print("finallist type:", type(strToList))

