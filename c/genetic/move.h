#pragma once
#ifndef MOVE_H
#define MOVE_H

#include <stdint.h>
#include <stdbool.h>

typedef struct {
	uint16_t m, n;
	uint8_t dir;
} move;

void move_init(move* move, uint16_t m, uint16_t n);
void move_flip_dir(move* move);
bool move_equiv(move move1, move move2);

#endif
