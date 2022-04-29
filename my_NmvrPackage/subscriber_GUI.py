import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import pygame
import csv
import subprocess

numOfDice = 15  # pocet buniek
widthHeight = 35  # vyska sirka grid samotnych buniek
margin = 5  # margin medzi bunkami

pygame.init()  # inicializacia pygame
pygame.display.set_caption("Subscriber GUI")  # Set title of screen
clock = pygame.time.Clock()  # obnovovanie displeja
screen = pygame.display.set_mode([630, 630])  # vyska sirka GUIcka - oknsa

robot_int_ort = [20, 21, 22, 23, 24, 25, 26, 27]

subprocess.Popen(['gnome-terminal', '-x', 'python3', '/home/nmvr/dev_ws/src/my_NmvrPackage/my_NmvrPackage/publisher_GUI_Dstar.py'])

class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10)
        self.subscription 

    def listener_callback(self, msg):
        grid = []  # 2d array pre mriezku
        # self.get_logger().info('I heard String: "%s"' % msg.data)
        print("Hearing String data...")
        data = msg.data       
        print("Converting String to list and showing grid...") 
        grid_p = data.split("-")
        for i in grid_p:
            grid.append(list(map(int, i[1:-1].split(", "))))
        
        for row in range(numOfDice):
            for column in range(numOfDice):
                color = (255, 255, 255)
                if grid[row][column] == 1: # mur
                    color = (30, 30, 30)
                for i in robot_int_ort: # robot
                    if grid[row][column] == i:
                        color = (255, 0, 0)
                if grid[row][column] == 3: # goal
                    color = (255, 255, 0)
                if grid[row][column] == 0: # free
                    color = (255, 255, 255)
                if grid[row][column] == 5:  # way
                    color = (30, 144, 255)
                pygame.draw.rect(screen, color, [(margin + widthHeight) * column + margin,
                                                (margin + widthHeight) * row + margin,
                                                widthHeight, widthHeight])
        clock.tick(60)  # 60 snimkov za sekundu
        pygame.display.flip()  # aktualizovat obrazovku podla vstupu co sme zaklikli
    
def main(args=None):
    rclpy.init(args=args)
    minimal_subscriber = MinimalSubscriber()
    rclpy.spin(minimal_subscriber)
    pygame.quit()
    minimal_subscriber.destroy_node()
    rclpy.shutdown()
    

if __name__ == '__main__':
    main()