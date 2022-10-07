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

int random_bounded(int min, int max){
	return (random() % (max - min)) + min;
}

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
	const uint16_t NUM_PATHS = random_bounded(100, 10000);
	//pointers and things
	person* init_pop = (person*)calloc(INIT_POP_SIZE, sizeof(person));
	person* next_pop;	//placeholder for each next population
	//additional variables
	int next_pop_size;	//placeholder for each next population size

	for(int i = 0; i < INIT_POP_SIZE; i++){
		person_init(&init_pop[i], LATTICE_SIZE[0], LATTICE_SIZE[1], NUM_PATHS);
		if(isinf(person_fitness(init_pop[i]))){
			person_show(init_pop[i]);
			printf("Size of population: %d\nC-value: %d\n", i + 1, 0);
		}
	}

	for(int gen = 0; gen < NUM_GENS; gen++){
		int current_pop_size;
		person* current_pop;
		if(!num_iters){	//only do this on the first round, when num_iters is 0
			current_pop = init_pop;
			current_pop_size = INIT_POP_SIZE;
		}
		else{
			current_pop = next_pop;
			current_pop_size = next_pop_size;
			//we only check fitness if this isn't init_pop because we already checked the fitness of that population
			for(int p = 0; p < current_pop_size; p++){
				if(isinf(person_fitness(current_pop[p]))){
					person_show(current_pop[p]);
					printf("Size of population: %d\nC-value: %d\n", current_pop_size, gen);
				}
			}
		}

		int num_duels;


	}

	return EXIT_SUCCESS;
}
