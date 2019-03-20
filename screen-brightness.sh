#!/bin/bash
#
# A small helper script to adjust the backlight on an ASUS X541NA
# Written by nootmuskaat

function show_usage() {
    >&2 echo "Usage: $0 [+|-]"
}

min() {
    local -ri first=$1
    local -ri second=$2
    echo $(( first < second ? first : second ))
}

max() {
    local -ri first=$1
    local -ri second=$2
    echo $(( first > second ? first : second ))
}

main() {
    local -r direction="$1"

    local -r backlight_dir=/sys/class/backlight/intel_backlight
    local -r current_value_file="${backlight_dir}/brightness"

    if [[ ! -d "${backlight_dir}" ]] ; then
        logger "ERROR: Cannot adjust brightness - no directory ${backlight_dir}"
        return 404
    fi

    local -ri min_brightness=0
    local -ri max_brightness=$(cat "${backlight_dir}/max_brightness")
    local -ri current_brightness=$(cat "${current_value_file}")

    local -i increment=$(( max_brightness / 20 ))
    increment=$(max ${increment} 1)

    local -i new_brightness=$(( current_brightness $direction increment ))
    new_brightness=$(min ${max_brightness} ${new_brightness})
    new_brightness=$(max ${min_brightness} ${new_brightness})

    echo ${new_brightness} > "${current_value_file}"
    if ! grep -q "^${new_brightness}$" "${current_value_file}" ; then
        logger "ERROR: Failed to set screen brightness"
        return 1
    fi

}

if [[ -z "$1" || "$1" == "-h" ]] ; then
    show_usage
    exit 0
elif [[ "$1" != "+" && "$1" != "-" ]] ; then
    >&2 echo "Invalid argument: '$1'"
    show_usage
    exit 1
fi

main "$@"
