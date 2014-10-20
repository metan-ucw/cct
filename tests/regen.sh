#!/bin/sh

for i in *.c.t; do
	../cct.py $i > ${i}.exp
done

rm -f *.c
