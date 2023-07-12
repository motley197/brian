cmake_minimum_required(VERSION 3.13)

# Initialise pico_sdk from installed location
# (note this can come from environment, CMake cache etc)
set(PICO_SDK_PATH "/home/motley/pico/pico-sdk")

set(PICO_BOARD pico_w CACHE STRING "Board type")
set(CMAKE_BUILD_TYPE Debug)
set(WIFI_SSID "MotleyFi")
set(WIFI_PASSWORD "DoloresWasHereAgain")

include(pico_sdk_import.cmake)

if (PICO_SDK_VERSION_STRING VERSION_LESS "1.4.0")
  message(FATAL_ERROR "Raspberry Pi Pico SDK version 1.4.0 (or later) required. Your version is ${PICO_SDK_VERSION_STRING}")
endif()

project(picow_blink C CXX ASM)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

pico_sdk_init()

add_executable(picow_blink
   picow_blink.c
)

pico_set_program_name(picow_blink "picow_blink")
pico_set_program_version(picow_blink "0.1")

pico_enable_stdio_usb(picow_blink 0)
pico_enable_stdio_uart(picow_blink 1)

pico_add_extra_outputs(picow_blink)

target_link_libraries(picow_blink pico_stdlib)

target_link_libraries(picow_blink
        pico_stdlib              # for core functionality
        pico_cyw43_arch_none     # we need Wifi to access the GPIO, but we don't need anything else
)

# Add the standard include files to the build
target_include_directories(picow_blink PRIVATE
  ${CMAKE_CURRENT_LIST_DIR}
  ${CMAKE_CURRENT_LIST_DIR}/.. # for our common lwipopts or any other standard includes, if required
)

# create map/bin/hex file etc.
pico_add_extra_outputs(picow_blink)


