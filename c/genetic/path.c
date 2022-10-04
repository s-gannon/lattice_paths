#include "path.h"
#include "move.h"

#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <assert.h>
#include <stdbool.h>

void path_init(path* path, uint16_t m, uint16_t n){
	assert(m > 0);
	assert(n > 0);

	path->m = m;
	path->n = n;
	path->moves = (move*)calloc(m + n, sizeof(move));

	move_init(&path->moves[0], 0, 0);
	for(int i = 1; i < path->m + path->n; i++){
		if((path->moves[i-1].m == m) && (path->moves[i-1].dir == EAST))
			move_flip_dir(&path->moves[i-1]);
		if((path->moves[i-1].n == n) && (path->moves[i-1].dir == NORTH))
			move_flip_dir(&path->moves[i-1]);
		move_init(
			&path->moves[i],
			path->moves[i-1].m + path->moves[i-1].dir,
			path->moves[i-1].n + (1 - path->moves[i-1].dir));
	}
}

void path_print(path path){
	for(int i = 0; i < path.m + path.n; i++){
		printf("%d %d %d\n",
		path.moves[i].m,
		path.moves[i].n,
		path.moves[i].dir);
	}
}

void path_print_converted(path path){
	for(int i = 0; i < path.m + path.n; i++)
		printf("%c", (path.moves[i].dir == EAST ? 'E' : 'N'));
	printf("\n");
}
//	A path is k-distinct from another if it shares fewer than k edges, or
//	k shared edges < k, then theye are k-distinct from one another. E;se, it
//	is k-equivalent to another path
bool path_k_equiv(path path1, path path2, uint16_t k){
	assert(path1.m == path2.m);
	assert(path1.n == path2.n);
	assert(k > 0);

	uint16_t k_shared = 0;

	for(int i = 0; i < path1.m + path1.n; i++)
		if(move_equiv(path1.moves[i], path2.moves[i]))
			k_shared++;
	if(k_shared < k)	//if num of edges shared is less than k, its k-dist
		return false;
	else
		return true;	//if num of edges is <= k, its k-equiv
}
