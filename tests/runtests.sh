#!/bin/sh

failcnt=0
verbose=1

print_diff()
{
	echo
	echo "Expected:"
	echo "---------"
	cat "$1" 2> /dev/null
	echo "---------"
	echo
	echo "Produced:"
	echo "---------"
	cat "$2" 2> /dev/null
	echo "---------"
	echo
}

for i in *.c.t *.h.t; do
	../cct.py "$i" &> log

	diff log ${i}.exp > /dev/null 2>&1
	if [ $? -ne 0 ]; then
		echo "$i errors Failed"
		failcnt=$((failcnt+1))

		if [ $verbose -eq 1 ]; then
			print_diff ${i}.exp log
		fi
	else
		echo "$i errors Succeded"
	fi
	rm log

	outfile=$(basename "$i" .t)

	if [ -e ${outfile}.exp ]; then
		diff $outfile ${outfile}.exp > /dev/null 2>&1
		if [ $? -ne 0 ]; then
			echo "$i output Failed"
			failcnt=$((failcnt+1))

			if [ $verbose -eq 1 ]; then
				print_diff ${outfile}.exp ${outfile}
			fi
		else
			echo "$i output Succeded"
		fi
	        rm -f $outfile
	fi
done

if [ $failcnt -gt 0 ]; then
	echo "Failed $failcnt testcases"
	exit 1
fi

echo
echo "All clear!"
exit 0
