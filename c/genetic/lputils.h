#ifndef LPUTILS_H
#define LPUTILS_H

#include <stddef.h>
#include <stdint.h>

//Returns the minimum unsigned 32-bit integers between `a` and `b`
uint32_t min_uint32(uint32_t a, uint32_t b);
//Returns the minimum double between `a` and `b`
double min_double(double a, double b);
//Softmax
double* softmax(double* x,  size_t x_size);
//Normalizes all of the numbers in `nums` and returns a list with length `size_nums`
double* normalize(double* nums, size_t size_nums);
//Returns the dot product of the two lists `nums1` and `nums2`
double* dot_product(double* nums1, double* nums2, double a, double b, size_t size_nums1, size_t size_nums2);

void bubble_sort(double* pivot, double* b, size_t size_pivot, size_t size_b);

void quick_sort(double* arr, size_t size_arr);

//Returns `n` factorial
uint32_t factorial(uint32_t n);
// Binomial coefficient of `m` choose `n`.
uint32_t combination(uint32_t n, uint32_t k);
#endif
