#!/usr/bin/env python3
import os, sys, getopt, time, string, json
#import netifaces as ni

def main():

    primaryLink = "10.120.0.1"
    secondaryLink = "10.121.0.1"
    bridgename = "testbr0"
    ifname = "vxlan0"
    local_ip = "10.120.0.3"
    waitsec = "0.5"
    pinginterval = 2
    pingcommand= "ping -c 1 -w "+waitsec+ " "
    helpdesk="linkwatch -p <primary tun dest ip> -s <secondary tun dest ip> -b <bridge> -i <vxlan name>"
    ofportFlow=""
    ofportNumber=""

    print("--------------------------------")
    print("Welcome to linkwatch SDN himmeli")
    print("--------------------------------")
    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:p:s:b:h", ["ifname","help", "primaryLink=", "secondaryLink=","bridgname="])
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
        elif opt in ("-i", "--ifname"):
            ifname = arg
    print("----------------------------------------------------------------------------------")
    while True:
        if(os.system(pingcommand + primaryLink)):
            if(os.system(pingcommand + primaryLink)):
        # Two pings before so that it does not flap unnecessarily
        # If secondaryLink is available we can save half a second of waiting
                if not (os.system(pingcommand + secondaryLink)):
                    print("Secondary link is available for usage")

                    ofportFlow=os.popen("ovsdb-tool query '[\"Open_vSwitch\", {\"op\":\"select\", \"table\":\"Interface\", \"where\": [[\"name\",\"==\",\""+ifname+"\"]]}]'").read()
                    
                    try:
                        ofportFlow=json.loads(ofportFlow)
                        ofportnumber=ofportFlow[0]["rows"][0]["ofport"]
                    except:
                        print("Something weird just happened, clearing all flows using the Floodlight cookie...")
                        os.system("ovs-ofctl del-flows "+bridgename + " cookie=0x20000000000000/-1")
                    else:
                        print("Clearing the flows in "+bridgename + " / " + ifname + " in port: " +ofportnumber)
                        os.system("ovs-ofctl del-rows "+bridgename+" out_ports="+ofportnumber)
                        

                while (os.system(pingcommand + primaryLink)):    # Lets run this forever or until the link is up
                    time.sleep(pinginterval)
                    pass

                print("-------------------------------------------------------------")
                print("The link is up again, continuing watching the primary link...")
                print("-------------------------------------------------------------")

        time.sleep(pinginterval)


if __name__ == "__main__":
    main()







#ofportNumber=ofportNumber[ofportNumber.rfind("\"ofport\":")+9:ofportNumber.rfind("\"ofport\":")+10]
