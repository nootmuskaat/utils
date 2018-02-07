#!/bin/bash
#
# A small helper script to adjust the backlight on an ASUS X541NA
# Written by nootmuskaat

function show_usage() {
    >&2 echo "Usage: $0 [+|-]"
}

if [ -z "$1" -o "$1" == "-h" ]; then
    show_usage
    exit 1
elif [ "$1" != "+" -a "$1" != "-" ]; then
    >&2 echo "Invalid argument: '$1'"
    show_usage
    exit 1
else
    DIRECTION=$1
fi

BACKLIGHT_DIR=/sys/class/backlight/intel_backlight
if [ ! -d $BACKLIGHT_DIR ]; then 
    logger "ERROR! $BACKLIGHT_DIR not found!"
    exit 404
fi

# This block should be adjusted to fit the max brightness
# of whatever the laptop model in question
MAX_BRIGHTNESS=$(cat $BACKLIGHT_DIR/max_brightness)
if [ $MAX_BRIGHTNESS -ne 96000 ]; then
    logger "ERROR! Max Brightness != 96000 found"
    exit 96
fi
INCR=960 # 1% total brightness

CURRENT=$(cat $BACKLIGHT_DIR/brightness)
NEW=$(expr $CURRENT $DIRECTION $INCR)

function set_brightness() {
    echo $1 > $BACKLIGHT_DIR/brightness
    # verify the unlikely scenario that the change didn't take effect
    NOW=$(cat $BACKLIGHT_DIR/brightness)
    if [ $NOW -ne $1 ]; then 
        return 1
    fi
}

if [ $NEW -ge 0 -a $NEW -le $MAX_BRIGHTNESS ]; then
    set_brightness $NEW || logger "Failed to adjust screen brightness" && exit 1
fi
