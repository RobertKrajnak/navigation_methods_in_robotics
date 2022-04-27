import pygame
import csv


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (30, 30, 30)

NumOfDice = 25
# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 20
HEIGHT = 20

# This sets the margin between each cell
MARGIN = 5
grid = [] # Create a 2 dimensional array. A two dimensional array is simply a list of lists.

# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [630, 630]
screen = pygame.display.set_mode(WINDOW_SIZE)

print("Zajdajte polohu robota v rozmedzi :", NumOfDice, "x", NumOfDice)
print("Zajdajte x-ovú súradnicu robota od 0 do ", NumOfDice-1, ":")
X_Robot = input()
print("Zajdajte y-ovú súradnicu robota od 0 do ", NumOfDice-1, ":")
Y_Robot = input()

for row in range(NumOfDice):
    # Add an empty array that will hold each cell
    # in this row
    grid.append([])
    for column in range(NumOfDice):
        grid[row].append(0)  # Append a cell

# with open("new_file.csv") as csvfile:
#     reader = csv.reader(csvfile) # change contents to floats
#     for row in reader: # each row is a list
#         grid.append(row)

grid[2][5] = 1# Set row 1, cell 5 to one. (Remember rows and column numbers start at zero.)
grid[int(X_Robot)][int(Y_Robot)] = 2# robot

pygame.init()# Initialize pygame

# FONT = pygame.font.Font("freesansbold.ttf", 20)
# button = pygame.Rect(5, 630, 310, 35)
# text_surf = FONT.render(str("SET ROBOT POSITION"), True, WHITE)
# text_rect = text_surf.get_rect(center=(155, 650))
# screen.blit(text_surf, text_rect)


pygame.display.set_caption("Array Backed Grid")# Set title of screen

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # User clicks the mouse. Get the position
            pos = pygame.mouse.get_pos()
            # Change the x/y screen coordinates to grid coordinates
            column = pos[0] // (WIDTH + MARGIN)
            row = pos[1] // (HEIGHT + MARGIN)

            # ak to nie je robot, tak viem editovat bunky
            if grid[row][column] != 2:
                # ak je 1 tak da 0 a opacne
                if grid[row][column] == 0:
                    grid[row][column] = 1
                else:
                    grid[row][column] = 0

            print("Click ", pos, "Grid coordinates: ", row, column, "Values:", grid[row][column])

            # print full actual grid
            for value_row in range(len(grid)):
                print(grid[value_row])

            # write actual grid to csv
            with open("new_file.csv", "w+", newline="") as my_csv:
                csvWriter = csv.writer(my_csv)
                csvWriter.writerows(grid)


    # Set the screen background
    # screen.fill(BLACK)

    # Draw the grid
    for row in range(NumOfDice):
        for column in range(NumOfDice):
            color = WHITE
            if grid[row][column] == 1:
                color = GRAY
            if grid[row][column] == 2:
                color = RED
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])

    # Limit to 60 frames per second
    clock.tick(60)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()