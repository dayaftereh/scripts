#include "linux_mac_address_reader.h"

LinuxMACAddressReader::LinuxMACAddressReader()
{ }

LinuxMACAddressReader::~LinuxMACAddressReader()
{ }

std::vector<std::string> LinuxMACAddressReader::getInterfaceNames()
{
    // list with all interface names
    std::vector<std::string> names;

    int n;
    struct ifaddrs *ifa;
    struct ifaddrs *ifaddr;

    // get all interface addresses
    if (getifaddrs(&ifaddr) == -1)
    {
        perror("getifaddrs");
        exit(EXIT_FAILURE);
    }

    // iterate of all interfaces
    for (ifa = ifaddr, n = 0; ifa != NULL; ifa = ifa->ifa_next, n++)
    {
        // check if nthe name is not null
        if (ifa->ifa_name != NULL)
        {
            // get the name
            std::string name(ifa->ifa_name);
            // add the name to list
            names.push_back(name);
        }
    }

    // free the interfaces
    freeifaddrs(ifaddr);

    return names;
}

std::string LinuxMACAddressReader::getMac(std::string interface)
{
    char buf[1024];

    struct ifreq ifr;
    struct ifconf ifc;

    // create a socket for accessing the interface's
    int sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_IP);
    if (sock == -1)
    {
        return std::string();
    }
    // set a buffer for getting the data
    ifc.ifc_len = sizeof(buf);
    ifc.ifc_buf = buf;

    // initialize the ifreq struct
    if (ioctl(sock, SIOCGIFCONF, &ifc) == -1)
    {
        return std::string();
    }
    // set the interface name to the ifreq
    strcpy(ifr.ifr_name, interface.data());

    // check if the ifr exists
    if (ioctl(sock, SIOCGIFFLAGS, &ifr) == 0)
    {
        // get the mac address
        if (ioctl(sock, SIOCGIFHWADDR, &ifr) == 0)
        {
            // create a new buf string for the mac address
            std::string buf;
            buf.resize(17);

            // convert the mac address to x:x:x:x:x:x
            snprintf((char *) buf.data(), 18, "%02x:%02x:%02x:%02x:%02x:%02x",
                     (uint8_t) ifr.ifr_hwaddr.sa_data[0], (uint8_t) ifr.ifr_hwaddr.sa_data[1],
                     (uint8_t) ifr.ifr_hwaddr.sa_data[2], (uint8_t) ifr.ifr_hwaddr.sa_data[3],
                     (uint8_t) ifr.ifr_hwaddr.sa_data[4], (uint8_t) ifr.ifr_hwaddr.sa_data[5]);

            return buf;
        }
    }

    return std::string();
}

std::vector<std::string> LinuxMACAddressReader::getMacAddresses()
{
    // the list for all mac addresses
    std::vector<std::string> addresses;
    // gets all interfaces names
    std::vector<std::string> names = this->getInterfaceNames();

    // get all interface names
    for (int i = 0; i < names.size(); ++i)
    {
        // get the name of the interface
        std::string name = names[i];
        // get the mac address for the interfaces
        std::string macAddress = this->getMac(name);
        // add the mac address to list
        addresses.push_back(macAddress);
    }

    return addresses;
}