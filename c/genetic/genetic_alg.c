#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <assert.h>
#include <stdbool.h>

enum dir {NORTH, EAST};

typedef struct {
	uint16_t m, n;
	uint8_t dir;
} move;

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

typedef struct {
	uint16_t m, n;
	move* moves;
} path;

void path_init(path* path, uint16_t m, uint16_t n){
	assert(m > 0);
	assert(n > 0);

	path->m = m;
	path->n = n;
	path->moves = (move*)calloc(m + n, sizeof(move));

	move_init(&path->moves[0], 0, 0);
	for(int i = 1; i < path->m + path->n; i++){
		if((&path->moves[i-1]->m == m) && (&path->moves[i-1]->dir == EAST))
			move_flip_dir(&path->moves[i-1]);
		if((&path->moves[i-1]->n == n) && (&path->moves[i-1]->dir == NORTH))
			move_flip_dir(&path->moves[i-1]);
		move_init(
			&path->moves[i],
			&path->moves[i-1]->m + &path->moves[i-1]->dir,
			&path->moves[i-1]->n + (1 - &path->moves[i-1]->dir));
	}
}

void path_print(path path){
	for(int i = 0; i < path.m + path.n; i++){
		printf("%d %d %d\n",
		path.moves[i]->m,
		path.moves[i]->n,
		path.moves[i]->dir);
	}
}

void path_print_converted(path path){
	for(int i = 0; i < path.m + path.n; i++)
		printf("%c", (path.moves[i]->dir == EAST ? 'E' : 'N'));
	printf("\n");
}
//	A path is k-distinct from another if it shares fewer than k edges, or
//	k shared edges < k, then theye are k-distinct from one another
bool path_k_dist(path path_1, path path_2, uint16_t k){
	assert(path_1.m == path_2.m);
	assert(path_1.n == path_2.n);
	assert(k > 0);

	uint16_t k_shared = 0;

	for(int i = 0; i < path_1.m + path.n; i++)
		if(move_equiv(path1.moves[i], path2.moves[i]))
			k_shared++;
	if(k_shared < k)
		return false;
	else
		return true;
}

typedef struct {
	uint16_t m, n;
	int num_paths;
	path* paths;
} person;

void person_init(person* person, uint16_t m, uint16_t n, int num_paths){
	//positivity asserts
	assert(m > 0);
	assert(n > 0);
	assert(num_paths > 0);

	person->paths = (path*)calloc(num_paths, sizeof(path));
	person->num_paths = num_paths;
	person->m = m;
	person->n = n;

	for(int i = 0; i < num_paths; i++)
		path_init(person->paths[i], m, n);
}

float person_fitness(person* person, int ){
	int penalty = 0;

	for(int i = 0; i < person->num_paths; i++){
		for(int j = i + 1; j < person->num_paths; j++){
			for(int k = 0; k < person->m + person->n; i++){
				if(!path_k_dist(person->paths[i], person->paths[j]))
					penalty++;
			}
		}
	}
	if(!penalty)	//will evaluate to true if penalty is 0
		return INFINITY;
	else
		return (1.0/penalty);
}

void person_show(person person){
	for(int i = 0; i < person.num_paths; i++){
		printf("Path #%d\n", i + 1);
		path_print(person.paths[i]);
		printf("\n");
	}
}

int main(int argc, char** argv){
	
	return EXIT_SUCCESS;
}
