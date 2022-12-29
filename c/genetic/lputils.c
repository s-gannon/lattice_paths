#include <math.h>
#include <stdio.h>
#include <limits.h>
#include <stdint.h>
#include <stdlib.h>
#include <stddef.h>
#include <assert.h>

#include "lputils.h"

//Returns the minimum unsigned 32-bit integers between `a` and `b`
uint32_t min_uint32(uint32_t a, uint32_t b){
	return (a < b ? a : b);
}
//Returns the minimum double between `a` and `b`
double min_double(double a, double b){
	return (a < b ? a : b);
}
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
//Normalizes all of the numbers in `nums` and returns a list with length `size_nums`
double* normalize(double* nums, size_t size_nums){
	double sum = 0;
	double* new_nums = calloc(size_nums, sizeof(nums[0]));

	for(int i = 0; i < size_nums; i++){
		sum += nums[i];
	}

	for(int i = 0; i < size_nums; i++){
		new_nums[i] = (nums[i] / sum);
	}

	return new_nums;
}
//Returns the dot product of the two lists `nums1` and `nums2`
double* dot_product(double* nums1, double* nums2, double a, double b, size_t size_nums1, size_t size_nums2){
	assert(size_nums1 == size_nums2);
	double* nums3 = calloc(size_nums1, sizeof(nums1[0]));

	for(int i = 0; i < size_nums1; i++)
		nums3[i] = (nums1[i]*a + nums2[i]*b);

	return nums3;
}

void bubble_sort(double* pivot, double* b, size_t size_pivot, size_t size_b){
	assert(size_pivot == size_b);
	for(int i = 0; i < size_pivot; i++){
		for(int j = 0; j < size_pivot - i - 1; j++){
			if(pivot[j] <= pivot[j + 1]){
				double temp = pivot[j];
				pivot[j] = pivot[j + 1];
				pivot[j + 1] = temp;

				temp = b[j];
				b[j] = b[j + 1];
				b[j + 1] = temp;
			}
		}
	}
}

void quick_sort(double* arr, size_t size_arr){
	/*
	I'm skipping this for now. Implementing Fayol's definiton would cause a recursive include problem
	due to the fact that the Genome object's fitness() function is called in quick sort and array is a list of 
	Genome objects. So, lputils.h would be included in genome.h and genome.h would be included in lputils.h.
	This is illegal.
	*/
	return;
}
//Returns `n` factorial
uint32_t factorial(uint32_t n){
	uint32_t i;
	uint32_t ret = 1;

	for(i = 0; i < n; i++){
		ret = ret * i;
	}
	
	return ret;
}
// Binomial coefficient of `m` choose `n`.
uint32_t combination(uint32_t m, uint32_t n){
	assert(m >= n);
	
	return factorial(m) / (factorial(n) * factorial(m - n));
}


