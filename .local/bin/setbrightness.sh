#!/bin/bash

# setbrightness - Control monitor brightness using ddcutil
# Usage: setbrightness <value>
# Value should be between 0-100

# Check if argument is provided
if [ $# -eq 0 ]; then
    echo "Usage: setbrightness <brightness_value>"
    echo "Brightness value should be between 0-100"
    echo "Current brightness:"
    ddcutil getvcp 10 2>/dev/null || echo "Error: Cannot detect monitor or ddcutil not installed"
    exit 1
fi

# Get the brightness value
brightness=$1

# Validate input is a number
if ! [[ "$brightness" =~ ^[0-9]+$ ]]; then
    echo "Error: Brightness value must be a number"
    exit 1
fi

# Validate range
if [ "$brightness" -lt 0 ] || [ "$brightness" -gt 100 ]; then
    echo "Error: Brightness value must be between 0-100"
    exit 1
fi

# Set brightness
echo "Setting brightness to $brightness%..."
if ddcutil setvcp 10 "$brightness" 2>/dev/null; then
    echo "Brightness set to $brightness%"
else
    echo "Error: Failed to set brightness. Make sure:"
    echo "1. ddcutil is installed"
    echo "2. Monitor supports DDC/CI"
    echo "3. You have proper permissions"
    exit 1
fi
