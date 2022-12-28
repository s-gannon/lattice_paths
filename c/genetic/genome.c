#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#include "lputils.h"
#include "sequence.h"
#include "genome.h"

void genome_init(genome_t* gen, uint16_t m, uint16_t n, uint16_t k, uint16_t num_sequences){
	gen->m = m;
	gen->n = n;
	gen->k = k;
	gen->num_sequences = num_sequences;
	gen->sequences = calloc(num_sequences, sizeof(sequence_t));

	for(int i = 0; i < num_sequences; i++){
		sequence_init(&gen->sequences[i], m, n);
	}
}	

void genome_generate_sequences(genome_t* gen){
	for(int i = 0; i < gen->num_sequences; i++){
		sequence_init(&gen->sequences[i], gen->m, gen->n);
	}
}
