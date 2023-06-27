# From Zero to Blinky World

This documentation summarises the steps to set up development for the Raspberry Pi Pico W and Debug Probe on Ubuntu 22.04 LTS

## Software Pre-requisites

The following packages need to be installed:

```
sudo apt update
sudo apt install build-essential git micro
sudo apt install cmake gcc-arm-none-eabi 
sudo apt install libnewlib-arm-none-eabi 
sudo apt install libstdc++-arm-none-eabi-newlib
```


## Hardware setup:

Both the Pico W and debug probe are connected to the host PC using USB.


![](../docs/img/wiring.jpeg)

# 1. Set up Pico SDK

The official documentation puts all pico code in a folder call `pico`

```
cd ~/
mkdir pico
cd pico
```

I use my `git` folder. It is entirely optional of course. Within this folder, there are a few repositories that need to be pulled down:

```
git clone https://github.com/raspberrypi/pico-sdk.git --branch master
cd pico-sdk
git submodule update --init
cd ..
git clone https://github.com/raspberrypi/pico-examples.git --branch master

```

## Modifications for Pico W

To avoid repetitive command line switches, the following changes are suggested:

### CMakeLists
All the examples have a top level CMakeLists.txt file. You can add some additional variables for the Pico W.

```
cd pico-examples
micro CMakeLists.txt
```

Under the line that reads `cmake_minimum_required(VERSION 3.12)` paste in the following (the micro editor uses ctrl-v for paste):

```
set(PICO_BOARD pico_w)
set(CMAKE_BUILD_TYPE Debug)
set(WIFI_SSID "<WIFI Network Name>")
set(WIFI_PASSWORD "<wifi password>")
```

Now press ctrl-S to save and ctrl-q to quit.



## Update the SDK

On occasion, you might want to pull any updated to the SDK

```
cd pico-sdk
git pull
git submodule update
```

