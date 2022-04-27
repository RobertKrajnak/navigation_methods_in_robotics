import os

def main():
    print("Yo")
    mydir = os.getcwd() + "/build/nmvrv2/build/lib/nmvrv2/"
    # os.system("gnome-terminal -e 'bash -c \"python3 " + mydir + "subzad.py; bash\"'")

    # os.system("gnome-terminal -e 'bash -c \"python3 " + mydir + "pubzad.py; bash\"'")

    os.system("gnome-terminal -e 'bash -c \"python3 " + mydir + "subscriberNewTest.py; bash\"'")

    os.system("gnome-terminal -e 'bash -c \"python3 " + mydir + "publisherDstar.py; bash\"'")


if __name__ == '__main__':
    main()
