#!/usr/bin/bash

manifesto=(
    zipshare.py
)

for i in ${manifesto[*]}; do
    cp -ufv $i ../bin
done
