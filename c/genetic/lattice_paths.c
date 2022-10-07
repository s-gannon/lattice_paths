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
		printf("Invalid number of arguments. Use %s m n k g s or run %s -h for help\n", argv[0], argv[0]);
		return EXIT_FAILURE;
	}
	//assert positive values for each
	for(int i = 1; i < argc; i++)
		assert(atoi(argv[i]) > 0);
	//seed srandom
	srandom(time(NULL));
	//start declaring and initializing vars
	//the variables from the command line
	const uint16_t LATTICE_SIZE[2] = {atoi(argv[1]), atoi(argv[2])};
	const uint16_t K_DIST = atoi(argv[3]);
	const uint16_t NUM_GENS = atoi(argv[4]);
	const uint16_t INIT_POP_SIZE = atoi(argv[5]);
	//randomized variables
	const uint16_t NUM_PATHS = (random() % 10000) + 100;
	//pointers and things
	person* init_pop = (person*)calloc(INIT_POP_SIZE, sizeof(person));

	for(int i = 0; i < INIT_POP_SIZE; i++){
		person_init(&init_pop[i], LATTICE_SIZE[0], LATTICE_SIZE[1], NUM_PATHS);
		if(isinf(init_pop[i])){
			person_show(init_pop[i]);
		}
	}

	for(int gen = 1; gen <= NUM_GENS; gen++){

	}

	return EXIT_SUCCESS;
}
