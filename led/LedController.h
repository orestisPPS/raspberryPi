/**
 * @file LEDController.h
 * @brief A class to control an LED using GPIO with blinking and dimming functionality.
 */

#ifndef LEDCONTROLLER_H
#define LEDCONTROLLER_H

#include <gpiod.h>
#include <string>

/**
 * @class LEDController
 * @brief Controls an LED connected to a GPIO pin.
 *
 * Provides functionality to initialize, blink, dim, and clean up GPIO resources for an LED.
 */
class LEDController {
public:
    /**
     * @brief Constructs an LEDController object.
     * @param pin GPIO pin number to control the LED.
     * @param chip_name Name of the GPIO chip device file. Default is "/dev/gpiochip0".
     */
    LEDController(unsigned pin, const std::string& chip_name = "/dev/gpiochip0");

    /**
     * @brief Destructor to release GPIO resources.
     */
    ~LEDController();
    /**
     * @brief Blinks the LED with a fixed interval.
     * @param interval_ms Blink interval in milliseconds.
     */
    void blink(unsigned interval_ms, unsigned cycles);

    /**
     * @brief Turns the LED on.
     */
    void on();

    /**
     * @brief Turns the LED off.
     */
    void off();


private:
    unsigned _pin;                      ///< GPIO pin number.
    std::string _chip_name;         ///< GPIO chip name.
    gpiod_chip* _chip;              ///< Handle for the GPIO chip.
    gpiod_line* _line;              ///< Handle for the GPIO line.

    /**
     * @brief Initializes the GPIO chip and line.
     * @return True if initialization was successful, false otherwise.
     */
    bool _init();

    /**
     * @brief Cleans up the GPIO resources.
     */
    void _cleanup();

    /**
     * @brief Sets the state of the LED.
     * @param on If true, turns the LED on; otherwise, turns it off.
     */
    void _setLEDState(bool on);
};

#endif // LEDCONTROLLER_H
