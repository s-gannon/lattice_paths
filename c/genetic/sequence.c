#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <assert.h>
#include <stdbool.h>

#include "sequence.h"

#define DEBUG_STATEMENTS true
#define SEEDED_RANDOM false

move generate_move(uint16_t m, uint16_t n){
	assert(m > 0 && n > 0);

	if(SEEDED_RANDOM)
		srand(time(NULL));
	
	return (move){.m = m, .n = n, .dir = (rand() % 2 == 0 ? NORTH : EAST)};	//ternary redundant, but more legible
}

void move_flip_dir(move* move){
	move->dir = (move->dir == EAST ? NORTH : EAST);
}

int move_compare(move mov1, move mov2){
	if(mov1.m == mov2.m){
		if(mov1.n == mov2.n){
			if(mov1.dir == mov2.dir){
				return 1;
			}
		}
	}

	return 0;
}


void sequence_init(sequence* seq, uint16_t m, uint16_t n){
	assert(m > 0 && n > 0);

	if(SEEDED_RANDOM)
		srand(time(NULL));

	seq->m = m;
	seq->n = n;
	seq->moves = (move*)calloc(m + n, sizeof(move));
	//we only allocate m + n moves since we know a path will always be m + n in length

	generate_move(0, 0);
	for(int i = 1; i < seq->m + seq->n; i++){
		if((seq->moves[i-1].m == m) && (seq->moves[i-1].dir == EAST))	//if we're all the way right, we can no longer go EAST
			move_flip_dir(&seq->moves[i-1]);
		if((seq->moves[i-1].n == n) && (seq->moves[i-1].dir == NORTH))	//if we're all the way up, we can no longer go NORTH
			move_flip_dir(&seq->moves[i-1]);
		generate_move(
			seq->moves[i-1].m + seq->moves[i-1].dir,
			seq->moves[i-1].n + (1 - seq->moves[i-1].dir));
	}

	return;
}

int sequence_compare(sequence seq1, sequence seq2, uint16_t k){
	assert(seq1.m == seq2.m && seq1.n == seq2.n);
	int k_equiv = 0;

	for(int i = 0; i < seq1.m + seq1.n; i++){
		if(move_compare(seq1.moves[i], seq2.moves[i]))
			k_equiv++;
	}

	if(k_equiv >= k)
		return 0;
	else
		return 1;
}

int sequence_same_paths(sequence seq1, sequence seq2){
	//to-do
	return 1;
}

void sequence_show(sequence seq, const int FORMAT){
	for(int i = 0; i < (seq.m + seq.n); i++){
		if(FORMAT == FMT_ENG)
			printf("%s", (seq.moves[i].dir == EAST ? "E" : "N"));
		else
			printf("%d %d %d\n", seq.moves[i].m, seq.moves[i].n, seq.moves[i].dir);
	}
	if(FORMAT == FMT_ENG)
		printf("\n");
	
	return;
}

	
