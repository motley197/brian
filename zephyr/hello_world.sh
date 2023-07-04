#!/bin/bash
cd ~/zephyrproject/zephyr
# From the root of the zephyr repository
west build -p always -b rpi_pico samples/basic/blinky
west build -p always -b rpi_pico samples/basic/blinky -- -DOPENOCD=/usr/local/bin/openocd -DOPENOCD_DEFAULT_PATH=/usr/local/share/openocd/scripts -DRPI_PICO_DEBUG_ADAPTER=cmsis-dap
