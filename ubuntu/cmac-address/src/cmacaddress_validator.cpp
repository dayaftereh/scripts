#include "cmacaddress_validator.h"

CMACAddressValidator::CMACAddressValidator()
{ }

CMACAddressValidator::~CMACAddressValidator()
{ }

// #################################################################

bool CMACAddressValidator::isValid()
{
    // if CMAC_ADDRESS is defined, then check for the mac address if exists
#ifdef CMAC_ADDRESS
    // create a new LinuxMACAddressReader
    LinuxMACAddressReader macAddressReader;
    // get a list with all MacAddresses
    std::vector<std::string> addresses = macAddressReader.getMacAddresses();

    // check if one mac address is equals to CMAC_ADDRESS
    for (int i = 0; i < addresses.size(); ++i)
    {
        std::string address = addresses[i];
        if (address.compare(CMAC_ADDRESS) == 0)
        {
            // if a mac address was found
            return true;
        }
    }
    // if not return false
    return false;
#endif
    // if no CMAC_ADDRESS is define, always return true
#ifndef CMAC_ADDRESS
    return true;
#endif
}

// #################################################################


bool CMACAddressValidator::validated()
{
    // create a MACAddressValidator
    CMACAddressValidator validator;
    // to the Mac Address validation
    return validator.isValid();
}
