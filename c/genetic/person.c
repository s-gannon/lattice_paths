#include "path.h"
#include "person.h"

#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <stdint.h>

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
		path_init(&person->paths[i], m, n);
}

float person_fitness(person* person, int k){
	int penalty = 0;

	for(int i = 0; i < person->num_paths; i++){
		for(int j = i + 1; j < person->num_paths; j++){
			if(path_k_equiv(person->paths[i], person->paths[j], k))
				penalty++;
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
