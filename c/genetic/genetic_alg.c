#include <math.h>
#include <time.h>
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
//	k shared edges < k, then theye are k-distinct from one another. E;se, it
//	is k-equivalent to another path
bool path_k_equiv(path path_1, path path_2, uint16_t k){
	assert(path_1.m == path_2.m);
	assert(path_1.n == path_2.n);
	assert(k > 0);

	uint16_t k_shared = 0;

	for(int i = 0; i < path_1.m + path.n; i++)
		if(move_equiv(path1.moves[i], path2.moves[i]))
			k_shared++;
	if(k_shared < k)	//if num of edges shared is less than k, its k-dist
		return false;
	else
		return true;	//if num of edges is <= k, its k-equiv
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
				if(path_k_equiv(person->paths[i], person->paths[j]))
					penalty++;
			}
		}
	}
	if(!penalty)	//if there are no k-equivalent paths, they're all k-dist
		return INFINITY;	//set fitness to infinity
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
	//check your argc and argv before running
	if(argc == 2 && !strncmp(argv[1], "-h", 2)){
		printf("Usage: ./%s m n k g s\n", argv[0]);
		printf("m, n : the width and height of the lattice\n");
		printf("   k : the k-distinctness we're looking for\n");
		printf("   g : the number of generations to run\n");
		printf("   s : the size of the initial population (I think?)\n");
		printf("\nRun ./%s -h to get this menu\n", argv[0]);
		return EXIT_SUCCESS;
	}
	else if(argc != 6){
		printf("Invalid number of arguments. Use ./%s m n k g s", argv[0]);
		return EXIT_FAILURE;
	}
	//assert positive values for each
	for(int i = 1; i < argc; i++)
		assert(argv[i] > 0);
	//seed srandom
	srandom(time(NULL));
	//start declaring and initializing vars
	//set our argvs to actual variables
	int lattice_size[2] = {(int)argv[1], (int)argv[2]};
	int k_dist_val = (int)argv[3];
	int num_generations = (int)argv[4];
	int pop_size = (int)argv[5];
	//create initial population
	person* current_pop = (person*)calloc(pop_size, sizeof(person));
	person* next_pop;
	//randomized variables
	int num_paths = (random() % 45) + 5;	//l in the paper
	int duel_coeff = random() % pop_size;	//delta_current
	int parent_coeff = (random() % duel_coeff)/2;	//alpha in the paper
	int mutation_coeff = ranom() % num_paths;		//mu in the paper

	return EXIT_SUCCESS;
}
