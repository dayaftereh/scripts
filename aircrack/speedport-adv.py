#!/usr/bin/python
import sys

def main(argv):
    if(len(argv) != 3):
        help()
        sys.exit(1)

    ssid, mac = argv[1], argv[2]
    mac = mac.replace(":", "").replace("-", "")

    input_key(ssid, mac)

    input_key(ssid.upper(), mac.upper())
    input_key(ssid.lower(), mac.lower())

    input_key(ssid.upper(), mac)
    input_key(ssid.lower(), mac)

    input_key(ssid, mac.upper())
    input_key(ssid, mac.lower())

    #input_2_key(ssid, mac)

def input_key(ssid, mac):
    for X in range(0, 10):
        for Y in range(0, 10):
            for Z in range (0, 10):
                key1 = ssid[9] + str(Z) + ssid[10] + mac[9:12] + str(X) + str(Y) + str(Z)
                output(key1)
                key2 = ssid[9]+str(Z)+ ssid[10]+str(ord(mac[8]))+str(ord(mac[9]))+str(ord(mac[10]))+str(X)+str(Y)+str(Z)+str(ord(ssid[6]))+ str(ord(ssid[7]))
                output(key2)

def input_2_key(ssid, mac):
    mac = str.upper(mac).replace(':', "")
    for X in range(0, 10):
        for Y in range(0, 10):
            for Z in range (0, 10):
                #print("SP-" + SSID[9] + str(Z) + SSID[10] + MAC[9:12] + str(X) + str(Y) + str(Z))
                output(key)

def output(key):
    print 'SP-' + key
    print 'SP-' + key.lower()
    print 'SP-' + key.upper()
    print key
    print key.lower()
    print key.upper()

def help():
    print( "usage: speed_port.py ssid mac")
    print(" ssid : WLAN-******")
    print(" mac  : **:**:**:**:**:**")

if __name__ == "__main__":
    main(sys.argv)
