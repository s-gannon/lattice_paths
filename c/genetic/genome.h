#ifndef GENOME_H
#define GENOME_H

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#include "lputils.h"
#include "sequence.h"

typedef struct{
	uint16_t m, n, k, num_sequences;
	sequence_t* sequences;
} genome_t;

//Initializes a new genome with `num_sequences` number of sequences (paths) which is made up of `m` by `n` lattices. The sequence length will always be length `m` times `n`.
void genome_init(genome_t* gen, uint16_t m, uint16_t n, uint16_t k, uint16_t num_sequences);

void genome_generate_sequences(genome_t* gen);

double genome_fitness();

double genome_divert();

void genome_show(genome_t genome);

void genome_mutate(genome_t genome);

void genome_n_mutate(genome_t genome);

#endif
