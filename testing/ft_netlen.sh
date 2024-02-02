#!/bin/bash
#
# Functional tests for netlen.py
# must be run from the same directory as netlen.py is located
#

TEXT=$(./netlen.py 10.10.10.10 8)
test "$TEXT" == "10.0.0.0 - 10.255.255.255" || echo "Bad output: \"$TEXT\""

TEXT=$(./netlen.py 10.10.10.10 16)
test "$TEXT" == "10.10.0.0 - 10.10.255.255" || echo "Bad output: \"$TEXT\""

TEXT=$(./netlen.py 10.10.10.10 24)
test "$TEXT" == "10.10.10.0 - 10.10.10.255" || echo "Bad output: \"$TEXT\""

TEXT=$(./netlen.py 10.10.10.10 33)
test "$TEXT" == "ERROR: mask not within range" || echo "Bad output: \"$TEXT\""

TEXT=$(./netlen.py 10.10.10.299 24)
test "$TEXT" == "ERROR: invalid address element '299'" || echo "Bad output: \"$TEXT\""

echo "OK"

exit 0
