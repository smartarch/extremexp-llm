#!/bin/bash

for i in {1..5}
do
    echo "Repetition: $i"
    echo
    
    python main.py 1
    python main.py 2
    python main.py 3
done