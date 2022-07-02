#!/bin/bash

rm -f data.txt
for instance in instances/*
do
  echo "$instance"
  python3 ./vertexcover.py "$instance" >> data.txt
done
