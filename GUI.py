import pygame
import csv
import os
import subprocess

numOfDice = 25  # pocet buniek
widthHeight = 20  # vyska sirka grid samotnych buniek
margin = 5  # margin medzi bunkami
grid = []  # 2d array pre mriezku
screen = pygame.display.set_mode([630, 630])  # vyska sirka GUIcka - oknsa
done = False  # pre ukoncenie GUI v cykle

pygame.init()  # inicializacia pygame
pygame.display.set_caption("Publisher GUI")  # Set title of screen
clock = pygame.time.Clock()  # obnovovanie displeja

print("Zajdajte polohu robota v rozmedzi :", numOfDice, "x", numOfDice)
print("Zajdajte x-ovú súradnicu robota od 0 do ", numOfDice - 1, ":")
x_Robot = input()
print("Zajdajte y-ovú súradnicu robota od 0 do ", numOfDice - 1, ":")
y_Robot = input()

subprocess.Popen(['gnome-terminal', '-x', 'python3', '/home/nmvr/dev_ws/src/my_NmvrPackage/my_NmvrPackage/publisher.py'])

for row in range(numOfDice):  # vytvorenie prazdneho 2d array s 0
    grid.append([])
    for column in range(numOfDice):
        grid[row].append(0)

grid[int(x_Robot)][int(y_Robot)] = 2  # pozicia robota robota z inputu - dvojka je robot

while not done:
    for event in pygame.event.get():  # vytvorenie eventu - ak sa nieco stlaci
        if event.type == pygame.QUIT:  # ak sa stlaci ukoncit
            done = True  # tak sa zmenit premenna a ukonci sa program
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()  # zisti poziciu mysi po kliknuti na ploche
            column = pos[0] // (widthHeight + margin)  # zmena súradnice obrazovky x/y na súradnice mriežky
            row = pos[1] // (widthHeight + margin)

            # ak to nie je robot, tak viem editovat bunky
            if grid[row][column] != 2:
                # ak je 1 tak da 0 a opacne - odklikavanie a zaklikavanie muru
                if grid[row][column] == 0:
                    grid[row][column] = 1
                else:
                    grid[row][column] = 0

            print("Click ", pos, "Grid coordinates: ", row, column, "Value:", grid[row][column])

            for value_row in range(len(grid)): # vykresli celú aktualnu mriežku
                print(grid[value_row])

            print("Saving data to csv...")
            with open("/home/nmvr/dev_ws/src/my_NmvrPackage/my_NmvrPackage/new_file.csv", "w+", newline="") as my_csv:  # zapíšte aktualnu mriežku do CSV
                csvWriter = csv.writer(my_csv)
                csvWriter.writerows(grid)

    for row in range(numOfDice):  # for pre vykreslenie mriezky
        for column in range(numOfDice):
            color = (255, 255, 255)  # biela pre nezakliknute
            if grid[row][column] == 1:
                color = (30, 30, 30)  # siva pre mury
            if grid[row][column] == 2:
                color = (255, 0, 0)  # cervena pre robota
            pygame.draw.rect(screen, color, [(margin + widthHeight) * column + margin,  # vykreslenie zafarbenia podla inputu
                                             (margin + widthHeight) * row + margin,
                                             widthHeight, widthHeight])

    clock.tick(60)  # 60 snimkov za sekundu
    pygame.display.flip()  # aktualizovat obrazovku podla vstupu co sme zaklikli

pygame.quit()
