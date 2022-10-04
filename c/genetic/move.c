#include "move.h"

#include <stdio.h>
#include <stdlib.h>

void move_init(move* move, uint16_t m, uint16_t n){
	move->m = m;
	move->n = n;
	move->dir = random() % 2;
}

void move_flip_dir(move* move){
	move->dir = 1 - move->dir;
}

bool move_equiv(move move1, move move2){
	return ((move1.m == move2.m) && (move1.n == move2.n) && (move1.dir == move2.dir));
}
