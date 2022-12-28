#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <assert.h>
#include <stdbool.h>

#include "sequence.h"

#define SEEDED_RANDOM false
#define DEBUG_STATEMENTS true

//	moves function

//Generates a new move given the (`m`, `n`) position. A random direction is chosen for each move generated.
move_t move_init(uint16_t m, uint16_t n){
	assert(m > 0 && n > 0);

	if(SEEDED_RANDOM)
		srand(time(NULL));	//only seeds with the time if the macro is true
	
	return (move_t){.m = m, .n = n, .dir = (rand() % 2 == 0 ? NORTH : EAST)};	//ternary redundant, but more legible
}
//Flips the direction of the move. If the move was directed `EAST`, it will be flipped `NORTH` and vice versa.
void move_flip_dir(move_t* move){
	move->dir = (move->dir == EAST ? NORTH : EAST);
}
//Compares two moves. Returns `1` if they are different and `0` if they are the same.
int move_compare(move_t mov1, move_t mov2){
	//checks move 1 for validity 
	assert(mov1.m > 0);
	assert(mov1.n > 0);
	assert(mov1.dir == EAST || mov1.dir == NORTH);
	//checks move 2 for validity 
	assert(mov2.m > 0);
	assert(mov2.n > 0);
	assert(mov2.dir == EAST || mov2.dir == NORTH);
	
	if(DEBUG_STATEMENTS)
		printf("[INFO] Comparing moves %d %d %c and %d %d %c...\n",
			mov1.m, 
			mov1.n, 
			mov1.dir == NORTH ? 'N' : 'E',
			mov2.m, 
			mov2.n, 
			mov2.dir == NORTH ? 'N' : 'E'
		);
	
	if(mov1.m == mov2.m){
		if(mov1.n == mov2.n){
			if(mov1.dir == mov2.dir){
				if(DEBUG_STATEMENTS)
					printf("[INFO] The moves are the same.\n");
				return 0;
			}
		}
	}
	if(DEBUG_STATEMENTS)
		printf("[INFO] The moves are different.\n");
	return 1;
}

//	sequences functions

//Initializes a new sequence (path) on an `m` by `n` lattice. The sequence length will always be length `m` times `n`.
void sequence_init(sequence_t* seq, uint16_t m, uint16_t n){
	assert(m > 0 && n > 0);

	if(SEEDED_RANDOM){
		if(DEBUG_STATEMENTS)
			printf("[INFO] Seeding sequence_init with current time...\n");
		srand(time(NULL));	//only seeds with the time if the macro is true
	}

	seq->m = m;
	seq->n = n;
	seq->moves = (move_t*)calloc(m + n, sizeof(move_t));
	//we only allocate m + n moves since we know a path will always be m + n in length

	move_init(0, 0);
	for(int i = 1; i < seq->m + seq->n; i++){
		if((seq->moves[i-1].m == m) && (seq->moves[i-1].dir == EAST))	//if we're all the way right, we can no longer go EAST
			move_flip_dir(&seq->moves[i-1]);
		if((seq->moves[i-1].n == n) && (seq->moves[i-1].dir == NORTH))	//if we're all the way up, we can no longer go NORTH
			move_flip_dir(&seq->moves[i-1]);
		move_init(
			seq->moves[i-1].m + seq->moves[i-1].dir,
			seq->moves[i-1].n + (1 - seq->moves[i-1].dir)
		);
	}

	return;
}
//Displays a sequence in either a numerical (`FMT_NUM`) or English (`FMT_ENG`) format. 
void sequence_show(sequence_t seq, const int FORMAT){
	for(int i = 0; i < (seq.m + seq.n); i++){
		if(FORMAT == FMT_ENG)
			printf("%s", (seq.moves[i].dir == EAST ? "E" : "N"));
		else	//FMT_NUM
			printf("%d %d %c\n", seq.moves[i].m, seq.moves[i].n, (seq.moves[i].dir == EAST ? 'E' : 'N'));
	}
	if(FORMAT == FMT_ENG)
		printf("\n");
	
	return;
}
//Compares two sequences together. If they are k-distinct, returns `1`, else if k-equivalent, returns `0` . 
int sequence_compare(sequence_t seq1, sequence_t seq2, uint16_t k){
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
//Compares two requences together. If they are identical, returns `1`, else returns `0`.
int sequence_same_paths(sequence_t seq1, sequence_t seq2){
	assert((seq1.m + seq1.n) == (seq2.m + seq2.n));	//m + n is the length of a path

	for(int i = 0; i < seq1.m + seq1.n; i++){
		if(move_compare(seq1.moves[i], seq2.moves[i]))
			return 0;
	}

	return 1;
}
