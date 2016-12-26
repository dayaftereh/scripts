#ifndef CMAC_ADDRESS_MACADDRESS_VALIDATOR_H
#define CMAC_ADDRESS_MACADDRESS_VALIDATOR_H

#include <assert.h>

#include "linux_mac_address_reader.h"

class CMACAddressValidator
{

public:

    CMACAddressValidator();

    virtual ~CMACAddressValidator();

private:

    bool isValid();

public:

    /**
     * checks if the defined CMAC_ADDRESS is equals
     * to one mac address of the interfaces
     *
     * @return true if a interface has the mac address CMAC_ADDRESS, otherwise false
     */
    static bool validated();

};


#endif //CMAC_ADDRESS_MACADDRESS_VALIDATOR_H
