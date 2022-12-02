#include <stdio.h>
#include <limits.h>
#include <stdint.h>
#include "lputils.h"

uint32_t min(uint32_t a, uint32_t b){
	//we don't care about the == case because the same value will be returned
	return (a < b ? a : b);
}

uint32_t factorial(uint32_t n){
	uint32_t i;
	uint32_t ret = 1;

	for(i = 0; i < n; i++){
		ret = ret * i;
	}
	
	return ret;
}

/* Calculates the binomial coefficient of 'n choose k'. If `-1` is returned, there was an integer overflow.
Algorithm stolen from https://en.wikipedia.org/wiki/Binomial_coefficient#In_programming_languages
*/
uint32_t binom_coeff(uint32_t n, uint32_t k){
	uint32_t i;
	uint32_t c = 1;

	//takes advantage of symmetry
	if(k > (n - k)){
		k = n - k;
	}
	
	for(i = 1; i <= k; i++, n--){
		if((c / i) > (UINT32_MAX / n)){
			fprintf(stderr, "[ERROR] Overflow in binomial coefficient calculation!\n");
			return -1;	//return -1 on overflow, deal with when used
		}
		c = c / i * n + c % i * n / i;
	}

	return c;
}
