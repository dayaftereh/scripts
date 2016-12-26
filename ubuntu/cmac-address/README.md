# CMAC-Address

CMAC-Address is a small and lightweight C++ Library for validating a Mac-Address from the System at Runtime-Time.
The Mac-Address can be define at Compile-Time by using CMake.
The idea of the Library is for simple protect own libraries and executable's for running on other systems.
This is not the best protection method to use the MAC-Address, because the MAC-Address can be spoofing, but it is simple and in same cases it makes a protection.

## Support Operating Systems

So far, the CMAC-Address Library is tested on the following Operating Systems.

 * **Ubuntu** (14.04)
 * **Raspbian** (Debian: 7.5, Kernel: 3.12.22+)
 
## Dependencies

The CMAC-Address Library has the following dependencies.

 * ```cmake``` 3.2+
 
## Usage

CMAC-Address is a C++ Library, which is compiled with CMake.
This mean the Library can easily included with CMake into own Projects.
For including the Library to a own Project, the git repository needs to be cloned into the project directory.
```
#> git clone https://github.com/dayaftereh/cmac-address.git cmac-address
```
For better understanding lets say we have the following project structure after cloning the git repository.
```
example
+-- cmac-address
    +-- src
        +-- ...
    +-- CMakeLists.txt
    +-- README.md
+-- src
    +-- main.cpp
+-- CMakeLists.txt
```
The File ```example/CMakeLists.txt``` needs to include the sub-directory ```cmac-address``` and define the executable for using the CMAC-Address Library.
The following shows a simple ```CMakeLists.txt``` File which helps to to explain how to include the Library.
```
cmake_minimum_required(VERSION 3.2)

# add the cmac-address library as subdirectory
add_subdirectory(cmac-address)

# define a new project with the name "example"
set(PROJECT_NAME "example")
project(${PROJECT_NAME})

# make the project as executable
add_executable(${PROJECT_NAME} src/main.cpp)

# link the cmac-address as library to the executable
target_link_libraries(${PROJECT_NAME} PUBLIC
        cmac-address
)
```
Now we need to use the CMAC-Library inside the source code.
The next code snippet shows, how to use the CMAC-Library inside the source code.
This code snippet presents the content of the ```example/src/main.cpp```
```
#include <cmacaddress_validator.h>

int main(int argc, char **argv)
{
    // check if MAC-Address is valid
    if(!CMACAddressValidator::validated()){
        // if not exit
        exit(EXIT_FAILURE);
    }
    // do other Stuff
    return EXIT_SUCCESS;
}
```
Now we can CMake and build the ```example```.

## Build

For building the ```example``` cmake requires same defines, because the MAC-Address which gets validated at Runtime, needs to be defined at the compile process.
The CMAC-Address Library use a MAC-Address which is defined for the preprocessor, which means the Address is hard coded into the binary.
First we need to create a ```build```-directory, for generating the Makefile's.
```
#> mkdir build
#> cd build
```
Now we can CMake and build the example Project with the CMAC-Address Library.
```
#> cmake ../
#> make -j4
```
This will build the ```example``` Project, without checking if a Mac-Address is valid and exists on the system, which means that ```CMACAddressValidator::validated()``` always returns ```true```.
The CMAC-Address Library allows to automatic grep a Mac-Address while Compile-Time.
This Mac-Address is then used to valid at Runtime-Time.
```
#> cmake -DCMAC_ADDRESS_AUTO=1 ../
#> make -j4
```
This will search for a **eth** or **wlan** network interface and use the first found mac-address.
If you system has no **eth** or **wlan** network interface, please use manual mac-address definition.
The next command shows, how to define manual a Mac-Address.
The Mac-Address needs the to be formatted as ```x:x:x:x:x:x``` in hexadecimal, like the linux system prints the Mac-Address.
```
#> cmake -DCMAC_ADDRESS=x:x:x:x:x:x ../
#> make -j4
```
This will hard code the given Mac-Adress ```x:x:x:x:x:x``` into the binary of the CMAC-Address Library.

