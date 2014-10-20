all: primes

primes: primes.h primes.c

clean:
	rm -f primes.h primes

CFLAGS+=-W -Wall

%.h: %.h.t
	../../cct.py $<
