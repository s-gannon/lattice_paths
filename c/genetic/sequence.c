#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stddef.h>
#include <limits.h>
#include <string.h>
#include <assert.h>
#include <stdbool.h>

#include "lputils.h"
#include "sequence.h"

#define SEEDED_RANDOM false
#define DEBUG_STATEMENTS true

//	moves function

//Generates a new move given the (`m`, `n`) position. A random direction is chosen for each move generated.
move_t move_init(uint32_t m, uint32_t n){
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
void sequence_init(sequence_t* self, uint32_t m, uint32_t n, sequence_t* paths, size_t len_paths, uint32_t index, bool empty){
	assert(m >= n);

	if(SEEDED_RANDOM){
		if(DEBUG_STATEMENTS)
			printf("[INFO] Seeding sequence_init with current time...\n");
		srand(time(NULL));	//only seeds with the time if the macro is true
	}

	self->m = m;
	self->n = n;
	self->length = m + n;
	self->num_moves = 0;
	self->moves = (move_t*)calloc(self->length, sizeof(move_t));

	if(!empty){
		self->path_index = ((index == UINT32_MAX) ? (rand() % len_paths) : index);
		self->moves = paths[self->path_index].moves;
	}
	else{

	}

	//My implementation of initializing moves randomly
	/*
	move_init(0, 0);
	self->num_moves++;
	for(int i = 1; i < self->length; i++){
		if((self->moves[i-1].m == m) && (self->moves[i-1].dir == EAST))	//if we're all the way right, we can no longer go EAST
			move_flip_dir(&self->moves[i-1]);
		if((self->moves[i-1].n == n) && (self->moves[i-1].dir == NORTH))	//if we're all the way up, we can no longer go NORTH
			move_flip_dir(&self->moves[i-1]);
		move_init(
			self->moves[i-1].m + self->moves[i-1].dir,
			self->moves[i-1].n + (1 - self->moves[i-1].dir)
		);
	}
	*/

	return;
}
//Displays a sequence in either a numerical (`FMT_NUM`) or English (`FMT_ENG`) format. 
void sequence_show(sequence_t seq, const int FORMAT){
	for(int i = 0; i < seq.length; i++){
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
int sequence_compare(sequence_t self, sequence_t seq, uint32_t k){
	assert((self.m == seq.m) && (self.n == seq.n));
	int k_equiv = 0;

	for(int i = 0; i < self.length; i++){
		if(move_compare(self.moves[i], seq.moves[i]))
			k_equiv++;
	}

	if(k_equiv >= k)
		return 0;
	else
		return 1;
}
//Compares two requences together. If they are identical, returns `1`, else returns `0`.
int sequence_same_paths(sequence_t self, sequence_t seq){
	assert(self.length == seq.length);	//m + n is the length of a path

	for(int i = 0; i < self.length; i++){
		if(move_compare(self.moves[i], seq.moves[i]))
			return 0;
	}

	return 1;
}

void sequence_generate_paths(uint32_t current_row, uint32_t current_col, sequence_t path, uint32_t m, uint32_t n, sequence_t* paths, size_t size_paths, const size_t MAX_PATHS_SIZE){
	assert(size_paths < MAX_PATHS_SIZE);

	if((current_row == m) && (current_col == n)){
		paths[size_paths++] = path;
		return;
	}

	if(current_row < m){

	}

	if(current_col < n){

	}
}

sequence_t* sequence_generate_all_paths(uint32_t m, uint32_t n){
	size_t max_length = combination(m + n, n);
	sequence_t empty;
	sequence_t* paths = calloc(max_length, sizeof(sequence_t));
	sequence_t* real_paths = calloc(max_length, sizeof(sequence_t));

	sequence_generate_paths(0, 0, empty, m, n, paths, 0, max_length);
	for(int i = 0; i < max_length; i++){
		real_paths[i] = paths[i];
	}

	return real_paths;
}

