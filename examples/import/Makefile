all: import.c

clean:
	rm -f import.c

%.c: %.c.t
	../../cct.py $<
