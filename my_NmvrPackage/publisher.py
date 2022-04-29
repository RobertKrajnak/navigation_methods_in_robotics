import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import csv

def readCSV():
    listToStr = ""
    grid = []
    row = 0
    print("Reading csv...")
    with open("/home/nmvr/dev_ws/src/my_NmvrPackage/my_NmvrPackage/new_file.csv") as csvfile:
        reader = csv.reader(csvfile) 
        for row in reader:
            grid_p = []
            for number in row:
                grid_p.append(int(number))
            grid.append(grid_p)
    print("Converting list to String...")
    listToStr = '-'.join([str(elem) for elem in grid])
    return listToStr

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        msg = String()
        msg.data = readCSV()
        self.publisher_.publish(msg)
        print("Publishing String data...")
        # self.get_logger().info('Publishing: "%s"' % msg.data)

def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher()
    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()