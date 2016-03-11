#!/usr/bin/env python3
import os, sys, getopt, time
#import netifaces as ni

def main():

    primaryLink = "10.120.0.1"
    secondaryLink = "10.121.0.1"
    bridgename = "testbr0"
#    ifname = "vxlan0"
#    termif = "tun0"
    waitsec = "0.5"
    pinginterval = 2
    pingcommand= "ping -c 1 -w "+waitsec+ " "
    helpdesk="linkwatch -p <primary tun dest ip> -s <secondary tun dest ip> -b <bridge>"

    counter = 0

    print("Welcome to linkwatch SDN himmeli")
    try:
        opts, args = getopt.getopt(sys.argv[1:], "p:s:b:h", ["help", "primaryLink=", "secondaryLink=","bridgname="])
    except getopt.GetoptError as err:
        print (err)
        print (helpdesk)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h' or opt == '--help':
            print (helpdesk)
            sys.exit()
        elif opt in ("-p", "--primary"):
            primaryLink = arg
        elif opt in ("-s", "--secondary"):
            secondaryLink = arg
        elif opt in ("-b", "--bridge"):
            bridgename = arg
    print("----------------------------------------------------------------------------------")
    while True:
        if(os.system(pingcommand + primaryLink)):
           if(os.system(pingcommand + primaryLink)):
        # If secondaryLink is available
              if not (os.system(pingcommand + secondaryLink)):
                  print("Secondary link is available for usage")
                  print("Clearing the flows from the bridge "+bridgename)
                  os.system("ovs-ofctl del-flows "+bridgename + " cookie=0x20000000000000/-1")
              else:
                  while (os.system(pingcommand + primaryLink)):    # Lets run this forever or until the link is up
                      time.sleep(5)
                      pass
        time.sleep(pinginterval)
        

if __name__ == "__main__":
    main()

