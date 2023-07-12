#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/timer.h"
#include "pico/cyw43_arch.h"

// GP4 and 28
const uint redLED = 28;
const uint greenLED = 4;

int64_t alarm_callback(alarm_id_t id, void *user_data) {
    // Put your timeout handler code in here
    puts("Coffee!");
    return 0;
}

uint8_t state = 1;
bool blinkMe(repeating_timer_t *rt) {
    // Put your timeout handler code in here
    gpio_put(greenLED, state);
    state = 1-state;
    return true;
}

int main()
{
    stdio_init_all();

    // Timer example code - This example fires off the callback after 2000ms
    add_alarm_in_ms(2000, alarm_callback, NULL, false);
    
    repeating_timer_t flashTmr = {0};
    add_repeating_timer_ms(500, blinkMe, NULL, &flashTmr);

    gpio_init(redLED);
    gpio_init(greenLED);
    gpio_set_dir(redLED, GPIO_OUT);
    gpio_set_dir(greenLED, GPIO_OUT);

    while (true) {
        gpio_put(redLED, 1);
        sleep_ms(175);
        gpio_put(redLED, 0);
        sleep_ms(175);
    }

    return 0;
}


