#pragma once
#ifndef PERSON_H
#define PERSON_H

#include "move.h"
#include <stdint.h>
#include <stdbool.h>

typedef struct {
	uint16_t m, n;
	move* moves;
} path;

enum dir {NORTH, EAST};

void path_init(path* path, uint16_t m, uint16_t n);
void path_print(path path);
void path_print_converted(path path);
bool path_k_equiv(path path1, path path2, uint16_t k);

#endif
