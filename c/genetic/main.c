#include "genome.h"
#include "sequence.h"
#include "population.h"

#include <math.h>
#include <time.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>
#include <assert.h>
#include <stdbool.h>

int main(int argc, char** argv){
	if(argc == 2 && !strncmp("-h", argv[1], 2)){
		fprintf(stdout, "[INFO] Run the command %s <value of m> <value of n> [name of file]\n", argv[0]);
		exit(EXIT_SUCCESS);
	}
	if(argc != 3 || argc != 4){
		fprintf(stderr, "[ERROR] Too %s arguments! Run %s -h for help.\n",
				(argc < 3 ? "few" : "many"),
				argv[0]);
		exit(EXIT_FAILURE);
	}

	const sequence_t* ALL_PATHS = sequence_generate_all_paths(argv[1], argv[2]);

	exit(EXIT_SUCCESS);
}
