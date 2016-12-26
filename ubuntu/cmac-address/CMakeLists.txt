cmake_minimum_required(VERSION 3.2)

# set the name of the library
set(PROJECT_NAME "cmac-address")
# define the cmac-address as project
project(${PROJECT_NAME}
        VERSION 0.1.0
        LANGUAGES C CXX
)

# define the PROJECT_DIRECTORY
set(PROJECT_DIRECTORY "${CMAKE_CURRENT_LIST_DIR}")
# get the Source Directory
set(SOURCE_DIRECTORY "${PROJECT_DIRECTORY}/src")

# get all headers and source files
file(GLOB_RECURSE HEADERS "${SOURCE_DIRECTORY}/*.h")
file(GLOB_RECURSE SOURCES "${SOURCE_DIRECTORY}/*.cpp")

# define the library cmac-address with the headers and source files
add_library(${PROJECT_NAME} ${HEADERS} ${SOURCES})

# define the include directory
target_include_directories(${PROJECT_NAME} PUBLIC
        ${SOURCE_DIRECTORY}
)

# fixing warning from cmake because undefined CMAC_ADDRESS_AUTO
message(STATUS "CMAC_ADDRESS_AUTO: ${CMAC_ADDRESS_AUTO}")

# check if auto mac-address is defined
if (DEFINED CMAC_ADDRESS_AUTO)
    # define the sys net directory for linux
    set(LINUX_SYS_NET "/sys/class/net")
    # check if the director exists
    if (NOT EXISTS ${LINUX_SYS_NET})
        message(FATAL "can't find [ ${LINUX_SYS_NET} ], please use manual mac-address definition")
    endif ()

    ## get all sub directoires
    file(GLOB IF_DIRS RELATIVE ${LINUX_SYS_NET} ${LINUX_SYS_NET}/*)

    # get a interface to get the mac address for
    foreach (IF_DIR ${IF_DIRS})
        # check if eth or wlan
        if (${IF_DIR} MATCHES "eth*" OR ${IF_DIR} MATCHES "wlan*")
            if (NOT DEFINED INTERFACE)
                set(INTERFACE "${IF_DIR}")
            endif ()
        endif ()
    endforeach ()

    # check if a INTERFACE was found
    if (NOT DEFINED INTERFACE)
        message(FATAL "cmake can't find a eth or wlan interface, please use manual mac-address definition")
    endif ()

    # define the file for the Hardware address
    set(IF_ADDRESS_FILE "${LINUX_SYS_NET}/${INTERFACE}/address")
    # check if the file exists
    if (NOT EXISTS ${IF_ADDRESS_FILE})
        message(FATAL "can't find [ ${IF_ADDRESS_FILE} ] for reading the haddress from interface [ ${INTERFACE} ]")
    endif ()

    # read the mac address
    file(STRINGS ${IF_ADDRESS_FILE} CMAC_ADDRESS)
    # define info in cmake
    message(STATUS "using the mac address [ ${CMAC_ADDRESS} ] of interface [ ${INTERFACE} ]")
endif ()

# fixing warning from cmake because undefined CMAC_ADDRESS
message(STATUS "CMAC_ADDRESS: ${CMAC_ADDRESS}")

# check if CMAC_ADDRESS is defined
if (DEFINED CMAC_ADDRESS)
    # display which mac address is used
    message(STATUS "using mac-address [ ${CMAC_ADDRESS} ] for validation")
    # give the MAC-Address to the preprocessor, for the hard coded mac-address check
    target_compile_definitions(${PROJECT_NAME} PRIVATE
            CMAC_ADDRESS="${CMAC_ADDRESS}"
    )
endif ()