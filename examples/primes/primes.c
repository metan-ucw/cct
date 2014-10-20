#include <stdio.h>
#include <stdlib.h>
#include "primes.h"

void print_fact(unsigned int val)
{
	unsigned int i, cnt;

	printf("%u = ", val);

	for (i = 0; i < sizeof(primes) / sizeof(*primes); i++) {
		cnt = 0;
		while (val % primes[i] == 0) {
			val /= primes[i];
			cnt++;
		}
		if (cnt)
			printf("%u^%u ", primes[i], cnt);
	}

	printf("\n");
}

int main(int argc, char *argv[])
{
	int i, val;

	for (i = 1; i < argc; i++)
		val = atoi(argv[i]);
		if (!val)
			printf("'%s' is not a number\n", argv[i]);
		else
			print_fact(val);

	return 0;
}
