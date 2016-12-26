#ifndef MAC_ADDRESS_I_MAC_READER_H
#define MAC_ADDRESS_I_MAC_READER_H

#include <string>
#include <vector>

class IMACReader
{
public:
    virtual ~IMACReader()
    { };

    /**
     * gets a list with all MacAddresses for all interfaces
     * @return a list with all MacAddresses from all interfaces
     */
    virtual std::vector<std::string> getMacAddresses() = 0;
};

#endif //MAC_ADDRESS_I_MAC_READER_H
