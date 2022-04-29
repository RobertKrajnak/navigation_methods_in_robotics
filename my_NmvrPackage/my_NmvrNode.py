import os 
import subprocess

def main():
    print('Running all scripts...')

    # subprocess.Popen(['gnome-terminal', '-x', 'python3', '/home/nmvr/dev_ws/src/my_NmvrPackage/my_NmvrPackage/turtle_gotogoal_node.py'])
    subprocess.Popen(['gnome-terminal', '-x', 'python3', '/home/nmvr/dev_ws/src/my_NmvrPackage/my_NmvrPackage/subscriber_GUI.py'])
    

if __name__ == '__main__':
    main()
