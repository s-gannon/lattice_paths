#include "move.h"
#include "path.h"
#include "person.h"

#include <math.h>
#include <time.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>
#include <assert.h>
#include <stdbool.h>

#define MINIMUM_PATHS 5

int main(int argc, char** argv){
	//check your argc and argv before running
	if(argc == 2 && !strncmp(argv[1], "-h", 2)){
		printf("Usage: %s m n k g s\n", argv[0]);
		printf("  m, n\t: the width and height of the lattice\n");
		printf("  k\t: the k-distinctness we're looking for\n");
		printf("  g\t: the number of generations to run\n");
		printf("  s\t: the size of the initial population (I think?)\n");
		printf("\nRun %s -h to get this menu\n", argv[0]);
		return EXIT_SUCCESS;
	}
	else if(argc != 6){
		printf("Invalid number of arguments. Use %s m n k g s\n", argv[0]);
		return EXIT_FAILURE;
	}
	//assert positive values for each
	for(int i = 1; i < argc; i++)
		assert(atoi(argv[i]) > 0);
	//seed srandom
	srandom(time(NULL));
	//start declaring and initializing vars
	//start with the constants (which are randomized at start)
	const int NUM_PATHS = (random() % 50) + MINIMUM_PATHS;	//l in the paper
	const int MUTATE_COEFF = random() % NUM_PATHS;			//mu in the paper
	//set our argvs to actual variables
	int lattice_size[2] = {atoi(argv[1]), atoi(argv[2])};
	int k_dist_val = atoi(argv[3]);
	int num_generations = atoi(argv[4]);
	int init_pop_size = atoi(argv[5]);
	//create initial population
	person* current_pop = (person*)calloc(init_pop_size, sizeof(person));
	person* next_pop;
	//randomized variables
	int duel_coeff = random() % init_pop_size;		//delta_goal
	int parent_coeff = (random() % duel_coeff)/2;	//alpha in the paper

	for(int i = 0; i < (random() % 500) + 100; i++){

	}


	return EXIT_SUCCESS;
}
