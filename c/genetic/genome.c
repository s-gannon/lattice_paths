#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#include "genome.h"
#include "lputils.h"
#include "sequence.h"

void genome_init(genome_t* self, size_t num_sequences, uint32_t m, uint32_t n, uint32_t k, genome_t* paths, size_t len_paths, bool empty){
	self->m = m;
	self->n = n;
	self->k = k;
	self->num_sequences = num_sequences;
	self->sequences = calloc(num_sequences, sizeof(sequence_t));

	for(int i = 0; i < num_sequences; i++){
		sequence_init(&gen->sequences[i], m, n);
	}
}	

void genome_generate_sequences(genome_t* gen){
	for(int i = 0; i < gen->num_sequences; i++){
		sequence_init(&gen->sequences[i], gen->m, gen->n);
	}
}
