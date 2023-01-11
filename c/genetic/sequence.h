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

typedef struct move_s{
	uint8_t dir: 2;		//the direction move is going
	uint32_t m;			//the horizontal position
	uint32_t n;			//the vertical position
	void* next;			//next move
} move_t;	//basically a linked list node

typedef struct sequence_s{
	uint32_t m;			//the horizontal length of lattice
	uint32_t n;			//the vertical length of lattice
	uint32_t length;	//length of the path (always m + n)
	uint32_t num_moves;	//number of moves currently in sequence
	uint32_t path_index;//index of the path fron ALL_PATHS
} sequence_t;	//linked list with extra steps

//	move functions

/*
Generates a new move given the (`m`, `n`) position. 
A random direction is chosen for each move generated.
*/
move_t move_init(uint32_t m, uint32_t n, uint8_t dir);
/*
Flips the direction of the move. 
If the move was directed `EAST`, it will be flipped `NORTH` and vice versa.
*/
void move_flip_dir(move_t* move);
/*
Compares two moves. 
Returns `1` if they are different and `0` if they are the same.
*/
int move_compare(move_t mov1, move_t mov2);
/*
Adds a move to the list.
*/
bool move_add(move_t* head, uint32_t m, uint32_t n, uint8_t dir);
/*
Removes a move from the list.
*/
bool move_remove(move_t* head, uint32_t m, uint32_t n, uint8_t dir);
//	sequence functionsz

/*
Initializes a new sequence (path) on an `m` by `n` lattice. 
If `index` is set to `UINT32_MAX`, then we will choose a random index.
If `ALL_PATHS` is `NULL`, then the sequence will be initialized as empty.
*/
void sequence_init(
	sequence_t* self, 
	uint32_t m, 
	uint32_t n, 
	const sequence_t* ALL_PATHS, 
	const size_t LEN_PATHS, 
	uint32_t index
);
//Displays a sequence in either a numerical (`FMT_NUM`) or English (`FMT_ENG`) format.
void sequence_show(sequence_t self, const int FORMAT);
/*
Compares two sequences together. 
If they are k-distinct, returns `1`, else if k-equivalent, returns `0`. 
*/
int sequence_compare(sequence_t self, sequence_t seq, uint32_t k);
/*
Compares two requences together. 
If they are identical, returns `1`, else returns `0`.
*/
int sequence_same_paths(sequence_t self, sequence_t seq);

//belong to lp_utils.py in the Python implementation

//Generates paths starting at the given `path`, `current_m`, and `current_n`.
void sequence_generate_paths(
	uint32_t current_m, 
	uint32_t current_n, 
	move_t path, 
	move_t* paths, 
	size_t size_paths, 
	const size_t MAX_PATHS_SIZE
);
//Generates all paths starting from (0,0) and going to (m,n).
move_t* sequence_generate_all_paths(uint32_t m, uint32_t n);

#endif
