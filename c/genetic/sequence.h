#ifndef SEQUENCE_H
#define SEQUENCE_H

#include <limits.h>
#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>

//	additional macros

#define NORTH 0
#define EAST  1

#define FMT_NUM 0
#define FMT_ENG 1

//	structures

typedef struct{
	uint32_t m, n;
	uint8_t dir: 1;
} move_t;

typedef struct{
	uint32_t m, n, length, path_index, num_moves;
	move_t* moves;
} sequence_t;

//	move functions

//Generates a new move given the (`m`, `n`) position. A random direction is chosen for each move generated.
move_t move_init(uint32_t m, uint32_t n, uint8_t dir);
//Flips the direction of the move. If the move was directed `EAST`, it will be flipped `NORTH` and vice versa.
void move_flip_dir(move_t* move);
//Compares two moves. Returns `1` if they are different and `0` if they are the same.
int move_compare(move_t mov1, move_t mov2);

//	sequence functions

//Initializes a new sequence (path) on an `m` by `n` lattice. The sequence length will always be length `m` times `n`.
void sequence_init(sequence_t* self, uint32_t m, uint32_t n, uint32_t index, const sequence_t* ALL_PATHS, const size_t LEN_PATHS);
//Displays a sequence in either a numerical (`FMT_NUM`) or English (`FMT_ENG`) format. 
void sequence_show(sequence_t self, const int FORMAT);
//Compares two sequences together. If they are k-distinct, returns `1`, else if k-equivalent, returns `0` . 
int sequence_compare(sequence_t self, sequence_t seq, uint32_t k);
//Compares two requences together. If they are identical, returns `1`, else returns `0`.
int sequence_same_paths(sequence_t self, sequence_t seq);

//belong to lp_utils.py in the Python implementation

void sequence_translate(sequence_t patA, const char* to_lan);

void sequence_generate_paths(uint32_t current_m, uint32_t current_n, sequence_t path, sequence_t* paths, size_t size_paths, const size_t MAX_PATHS_SIZE);

sequence_t* sequence_generate_all_paths(uint32_t m, uint32_t n);

#endif
