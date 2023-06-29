# From Zero to Blinky World

This documentation summarises the steps to set up development for the Raspberry Pi Pico W and Debug Probe on Ubuntu 22.04 LTS

## Software Pre-requisites

The following packages need to be installed:

```
sudo apt update
sudo apt install build-essential git micro pkg-config git-lfs minicom
sudo apt install cmake gcc-arm-none-eabi 
sudo apt install libnewlib-arm-none-eabi 
sudo apt install libstdc++-arm-none-eabi-newlib
sudo apt install automake autoconf build-essential texinfo libtool libftdi-dev 
sudo apt install libusb-1.0-0-dev
sudo apt install python3-dev python3-pip
sudo apt install gdb-multiarch
```

## Hardware setup:

Both the Pico W and debug probe are connected to the host PC using USB.


![](../docs/img/wiring.jpeg)

# 1. Set up Pico SDK and Related Tools

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
git clone https://github.com/raspberrypi/pico-project-generator
git clone https://github.com/raspberrypi/picotool.git --branch master
git clone https://github.com/raspberrypi/openocd.git --branch rp2040 --recursive --depth=1
git clone https://github.com/raspberrypi/picoprobe.git
cd picoprobe
git submodule update --init
cd ..
```

To build the forked version of `openocd` (supports Pico dual-core), do the following:

```
cd ~/pico
cd openocd
./bootstrap
./configure
make -j4
sudo make install
cd ..
```

> *NOTE* 
>
> I have also seen `./configure --enable-ftdi --enable-sysfsgpio --enable-bcm2835gpio` which I *think* is needed for the Raspberry Pi based SWD.

To build `picotool`, do the following:

```
cd ~/pico
cd picotool
mkdir build
cd build
cmake ..
make -j4
sudo make install
cd ..
```

To build `picoprobe`, do the following:

```
cd ~/pico
cd picoprobe
mkdir build && cd build
cmake ..
make -j4
cd ..
```

## Modifications for Pico W

To avoid repetitive command line switches, the following changes are suggested:

### CMakeLists
All the examples in the pico-examples repository are built using a top level file `CMakeLists.txt` file. You can add some additional variables to this file so that it builds for the Pico W and supports debugging.

```
cd ~/pico
cd pico-examples
micro CMakeLists.txt
```

Under the line that reads `cmake_minimum_required(VERSION 3.12)` paste in the following (the micro editor uses ctrl-v for paste) and edit the WiFi strings accordingly:

```
set(PICO_BOARD pico_w)
set(CMAKE_BUILD_TYPE Debug)
set(WIFI_SSID "<WIFI Network Name>")
set(WIFI_PASSWORD "<wifi password>")
```

Now press ctrl-S to save and ctrl-q to quit.

## Set `PICO_SDK_PATH`

Once again, so save a lot of typing (and typos!) you should set the `PICO_SDK_PATH` in your bash profile. Each time you open a terminal, this will be set.

You can do this by typing the following (only do this once!):

```
echo "export PICO_SDK_PATH=$HOME/pico/pico-sdk" >> ~/.bashrc
```

## UDEV Permissions

The pico probe is a USB device that requires sudo (or root) privileges to access. This again can be problematic when performing debugging. To give all users access to this device, so the following:

```
sudo micro /etc/udev/rules.d/50-pico-debug-probe.rules 
```

Paste the following:

```
# Pico Debug Probe
SUBSYSTEM=="usb", ATTRS{idVendor}=="2e8a", ATTRS{idProduct}=="000c", MODE="666", GROUP="plugdev"
```

> You might want to check the vendor and product IDs are correct
>
> `lsusb | grep -i raspberry`
> 
> Check the ID. It is in the format vendor:product

Now either reboot, or type the following:

```
sudo udevadm control --reload
sudo udevadm trigger
```

## Build and Run the Examples

To build all examples, you now simply need to perform the following:

```
cd ~/pico
cd pico-examples
rm -rf build && mkdir build
cd build
cmake ..
make -j4
ls
```

Staying in this `build` folder, we see all the subfolders containing corresponding makefiles for each example. For example, let's build the pico_w version of blinky:

```
cd ~/pico/pico-examples/build/pico_w/wifi/blink
make -j4
ls
```

You should see both `picow_blink.elf` (for debugging) and `picow_blink.uf2` (for drag-drop programming)

### Run the Code - drag and drop

* Disconnect the usb cable to the pico_w
* Hold the button and reconnect. The pico_w will mount as a mass storage device (much like a USB stick).
* Drag `picow_blink.uf2` into the windows that pops up


To see cause and effect, let's change the blink rate. The source files are in a different tree:

```
micro ~/pico/pico-examples/pico_w/wifi/blink/picow_blink.c
```

Again, ctrl-s to save and ctrl-q to quit. Try changing the delay, and re-build with `make -j4`

Now deploy again to see the change!

### Run the code - debug probe

The drag-drop method is tedious, and will cause wear on the connectors. Better is to use the debug probe:

```
sudo openocd -f interface/cmsis-dap.cfg -f target/rp2040.cfg -c "adapter speed 5000" -c "program picow_blink.elf verify reset exit"
```

If you changed the [UDEV permissions](#udev-permissions), then you can drop `sudo` (yipee :). It is possible this might help integrating debug into an IDE (to be proven)


### Debug the Code in a Terminal (using the pico debugger)

It is useful to be able to single step code, set breakpoints and inspect variables. Of course, an IDE should make this a relatively seamless experience (assuming you can set one up). However, it is useful to see it in action at command line level.

First open **an additional** terminal and run the following command.

```
cd ~/pico/pico-examples/build/pico_w/wifi/blink
sudo /usr/local/bin/openocd -f interface/cmsis-dap.cfg -f target/rp2040.cfg -c "adapter speed 5000"
```

Again, you might be able to drop the `sudo`. You can leave this running for the duration of your development session.

From a different terminal, you can now run the following:

```
cd ~/pico/pico-examples/build/pico_w/wifi/blink
gdb-multiarch picow_blink.elf
```

Connect to the debugger (listening on port 3333)

```
(gdb) target remote localhost:3333
```

Load code into flash

```
(gdb) load
```

Now set a breakpoint in main and start it running

```
(gdb) monitor reset init
(gdb) b main
(gdb) continue
```
## Create a new project for debugging in Visual Studio Code

The official documentation does not say much about the cmsis-dap "Debug Probe". 

There are a couple options however:

### Start the debugger manually
What seems to work well is to start `openocd` manually (as above) and connect to it as a remote debugger.

Given all the above, the steps are probably easier to show than write. The following video hopefully captures it.

https://youtu.be/T09zMnDtpZ4

### The pico-project-generate tool
There is a really neat little tool to create projects and starter code for the pico and pico_w. It also includes an option to generate project files for VS Code

https://github.com/raspberrypi/pico-project-generator

Unfortunately, cmcsis-dap debig probe is not offically supported at the time of writing, so as an interim, you can try using our fork for this project 

https://github.com/noutram/pico-project-generator 

To build a project using the gui tool 

```
cd pico
mkdir forks
cd forks
git clone https://github.com/noutram/pico-project-generator
./pico_project.py --gui
```

Note this is not yet fuly tested. I've sent some PULL REQUESTS to add support for the debug probe. 

For the pico examples, https://github.com/raspberrypi/pico-examples/pull/401
For the pico project generator, https://github.com/raspberrypi/pico-project-generator/pull/76

### The written and slightly more verbose version

So again, start the debug server in a separate terminal:

```
sudo openocd -f interface/cmsis-dap.cfg -f target/rp2040.cfg -c "adapter speed 5000"
```

A pre-built project has been [included in this repository](../blink/). You can [see the project files here](https://github.com/motley197/brian/tree/main/picow/blink)

In a terminal, navigate to the blink folder (part of this repository, /picow/blink) and type the following:

```
rm -rf build
code .
```

At the bottom of the screen, you may need to choose a "kit" (arm-none-eabi) and set the CMake build variant to debug.

Now select the Debug view (ctrl-shift-D). At the top of the screen is a small green arrow. Clicking this should build and debug.

*A little information on how this was set up*

I first used the "Pico Project Generator" to create a basic project:

```
cd ~/pico/pico-project-generator/
./pico_project.py --gui
```

* The files were moved out, and **the build folder was deleted**.
* The `.vscode` sub-folder contains two files: `launch.json` and `settings.json`. These were derived from the examples in the SDK folder `~/pico/pico-examples/ide/vscode/`
   * for `launch.json`, I've copied `launch-remote-openocd.json`
* The `CMakeLists.txt` was modified.

The `CMakeLists.txt` file reads as follows:

```cmake
cmake_minimum_required(VERSION 3.13)

# Initialise pico_sdk from installed location
# (note this can come from environment, CMake cache etc)
set(PICO_SDK_PATH "/home/myusername/git/pico-sdk")  # CHANGE THIS!!!
set(PICO_BOARD pico_w CACHE STRING "Board type")
set(CMAKE_BUILD_TYPE Debug)
set(WIFI_SSID "<wifi SSID>")  # CHANGE THIS!!
set(WIFI_PASSWORD "<wifi password>") # CHANGE THIS!!

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

```

Then leave VS Code to do the rest.

## Update the SDK

On occasion, you might want to pull any updated to the SDK

```
cd pico-sdk
git pull
git submodule update
```

