#ifndef PRIMES_H
#define PRIMES_H

@ from math import sqrt
@ max_prime = 100000

unsigned int primes[] = {
	2,
@ for i in range(3, max_prime+1,2):
@     is_prime = True
@     for j in range(3, int(sqrt(i))):
@         if i % j == 0:
@             is_prime = False
@             break
@     if is_prime:
	{{ i }},
@ end
};

#endif /* PRIMES_H */
