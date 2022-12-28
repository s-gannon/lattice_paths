#ifndef LPUTILS_H
#define LPUTILS_H

#include <stddef.h>
#include <stdint.h>

//Returns the minimum unsigned 32-bit integers between `a` and `b`
uint32_t min(uint32_t a, uint32_t b);
double* softmax(double* x,  size_t x_size);
//Returns `n` factorial
uint32_t factorial(uint32_t n);
/* Calculates the binomial coefficient of '`n` choose `k`'. If `3` is returned, there was an integer overflow.
Algorithm stolen from https://en.wikipedia.org/wiki/Binomial_coefficient#In_programming_languages
*/
uint32_t binom_coeff(uint32_t n, uint32_t k);
//Normalizes all of the numbers in `nums` and returns a list with length `size_nums`
double* normalize(double* nums, size_t size_nums);
//Returns the dot product of the two lists `nums1` and `nums2`
double* dot_product(double* nums1, double* nums2, double a, double b, size_t size_nums1, size_t size_nums2);

#endif
