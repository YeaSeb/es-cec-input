#!/bin/bash

echo "killing cec-client and python3 before restarting es-cec-input"
killall python3
killall cec-client -s KILL
systemctl --user restart es-cec-input
