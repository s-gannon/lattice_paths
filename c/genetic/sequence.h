#ifndef SEQUENCE_H
#define SEQUENCE_H

#include <limits.h>
#include <stdint.h>

//	additional macros

#define NORTH 0
#define EAST  1

#define FMT_NUM 0
#define FMT_ENG 1

//	structures

typedef struct{
	uint16_t m, n;
	uint16_t dir: 1;
} move;

typedef struct{
	uint16_t m, n;
	move* moves;
} sequence;

//	move functions

//Generates a new move given the (`m`, `n`) position. A random direction is chosen for each move generated.
move generate_move(uint16_t m, uint16_t n);
//Flips the direction of the move. If the move was directed `EAST`, it will be flipped `NORTH` and vice versa.
void move_flip_dir(move* move);
//Compares two moves. Returns `0` if they are different and `1` if they are the same.
int move_compare(move mov1, move mov2);

//	sequence functions

//Initializes a new sequence (path) on an `m` by `n` lattice. The sequence length will always be length `m` times `n`.
void sequence_init(sequence* seq, uint16_t m, uint16_t n);
//Compares two sequences together. If they are k-distinct, returns `1`, else returns `0`. 
int sequence_compare(sequence seq1, sequence seq2, uint16_t k);
//Compares two requences together. If they are identical, returns `1`, else returns `0`.
int sequence_same_paths(sequence seq1, sequence seq2);
//Displays a sequence in either a numerical (`FMT_NUM`) or English (`FMT_ENG`) format. 
void sequence_show(sequence seq, const int FORMAT);

#endif
