#!/usr/bin/env bash

FILE=$1

while read RECORD; do
    cat $RECORD
done < $FILE
