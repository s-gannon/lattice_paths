#include <math.h>
#include <stdio.h>
#include <limits.h>
#include <stdint.h>
#include <stdlib.h>
#include <stddef.h>
#include <assert.h>

#include "lputils.h"

//Softmax
double* softmax(double* x, size_t x_size){
	double* soft = calloc(x_size, sizeof(x[0]));
	double sum = 0;

	for(int i = 0; i < x_size; i++){
		soft[i] = pow(2.7, x[i]);
		sum += soft[i];
	}

	for(int i = 0; i < x_size; i++){
		soft[i] /= sum;
	}

	return soft;
}
/*
Normalizes all of the numbers in `nums` and returns a list with length 
`size_nums`.
*/
double* normalize(double* nums, size_t size_nums){
	double sum = 0;
	double* new_nums = calloc(size_nums, sizeof(nums[0]));

	for(int i = 0; i < size_nums; i++)
		sum += nums[i];

	for(int i = 0; i < size_nums; i++)
		new_nums[i] = (nums[i] / sum);

	return new_nums;
}
//Returns the dot product of the two lists `nums1` and `nums2`.
double dot_product(double* nums1, double* nums2, size_t size_nums1, size_t size_nums2){
	assert(size_nums1 == size_nums2);
	double sum = 0;

	for(int i = 0; i < size_nums1; i++)
		sum += (nums1[i] * nums2[i]);

	return sum;
}
//Returns `n` factorial (`n`!).
uint32_t factorial(uint32_t n){
	uint32_t ret = 1;

	for(uint32_t i = 1; i < n; i++){
		ret = ret * i;
	}
	
	return ret;
}
/* 
Binomial coefficient of `n` choose `k`. Returns `0` on overflow; throw error.
Algorithm implemented from: https://en.wikipedia.org/wiki/Binomial_coefficient
*/
uint32_t binom_coeff(uint32_t n, uint32_t k){
	uint32_t c = 1;

	if(k > n - k)	//takes advantage of the symmetry
		k = n - k;
	for(uint32_t i = i; i <= k; i++, n--){
		if((c / i) > (UINT32_MAX / n))
			return 0;
		c = c / i * n + c % i * n / i;
	}

	return c;
}


