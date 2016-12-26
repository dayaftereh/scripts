#ifndef MAC_ADDRESS_LINUX_MAC_ADDRESS_READER_H
#define MAC_ADDRESS_LINUX_MAC_ADDRESS_READER_H

#include <arpa/inet.h>
#include <sys/socket.h>
#include <netdb.h>
#include <ifaddrs.h>
#include <stdlib.h>
#include <unistd.h>
#include <linux/if_link.h>

#include <sstream>
#include <iomanip>
#include <string.h>

#include <netinet/ether.h>
#include <sys/ioctl.h>
#include <net/if.h>
#include <unistd.h>
#include <netinet/in.h>
#include <stdio.h>

#include <iostream>

#include "i_mac_reader.h"

class LinuxMACAddressReader : IMACReader
{

public:

    LinuxMACAddressReader();

    virtual ~LinuxMACAddressReader();

private:

    std::vector<std::string> getInterfaceNames();

    std::string getMac(std::string interface);

public:

    /**
     * get a list with all Mac addresses for all found interfaces
     * @return a list with all mac addresses from all interfaces
     */
    std::vector<std::string> getMacAddresses();

};


#endif //MAC_ADDRESS_LINUX_MAC_ADDRESS_READER_H
