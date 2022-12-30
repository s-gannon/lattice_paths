#ifndef LPUTILS_H
#define LPUTILS_H

#include <stddef.h>
#include <stdint.h>

//Softmax algorithm
double* softmax(double* x,  size_t x_size);
//Normalizes all of the numbers in `nums` and returns a list with length `size_nums`
double* normalize(double* nums, size_t size_nums);
//Returns the dot product of the two lists `nums1` and `nums2`
double dot_product(double* nums1, double* nums2, size_t size_nums1, size_t size_nums2);
//Returns `n` factorial
uint32_t factorial(uint32_t n);
// Binomial coefficient of `m` choose `n`.
uint32_t binom_coeff(uint32_t n, uint32_t k);
#endif
