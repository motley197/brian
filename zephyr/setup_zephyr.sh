#!/bin/bash

wget https://apt.kitware.com/kitware-archive.sh
sudo bash kitware-archive.sh

sudo apt install --no-install-recommends git cmake ninja-build gperf \
  ccache dfu-util device-tree-compiler wget \
  python3-dev python3-pip python3-setuptools python3-tk python3-wheel xz-utils file \
  make gcc gcc-multilib g++-multilib libsdl2-dev libmagic1

cmake --version
python3 --version
dtc --version  

sudo apt install python3-venv

mkdir -p ~/zephyrproject
cd ~/zephyrproject
mkdir -p ~/zephyrproject/.venv
python3 -m venv ~/zephyrproject/.venv
source ~/zephyrproject/.venv/bin/activate
echo "run deactivate to quite the venv"

pip install west
west init ~/zephyrproject
cd ~/zephyrproject
west update

# Create CMake package
rm -rf ~/.cmake/packages/ZephyrUnittest 
rm -rf ~/.cmake/packages/Zephyr
west zephyr-export
# Zephyr (/home/noutram/zephyrproject/zephyr/share/zephyr-package/cmake) has been added to the user package registry in: ~/.cmake/packages/Zephyr
# ZephyrUnittest (/home/noutram/zephyrproject/zephyr/share/zephyrunittest-package/cmake) has been added to the user package registry in: ~/.cmake/packages/ZephyrUnittest

pip install -r ~/zephyrproject/zephyr/scripts/requirements.txt

