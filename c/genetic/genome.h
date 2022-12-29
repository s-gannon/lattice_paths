#ifndef GENOME_H
#define GENOME_H

#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>

#include "lputils.h"
#include "sequence.h"

typedef struct{
	uint32_t m, n, k, num_sequences;
	sequence_t* sequences;
} genome_t;

//Initializes a new genome with `num_sequences` number of sequences (paths) which is made up of `m` by `n` lattices. The sequence length will always be length `m` times `n`.
void genome_init(genome_t* self, size_t num_sequences, uint32_t m, uint32_t n, uint32_t k, genome_t* paths, size_t len_paths, bool empty);

void genome_generate_sequences(genome_t* self, genome_t* paths, size_t len_paths, bool empty);

double genome_fitness(genome_t* self, type_t dict_equivalences, bool penalty_indexes);	

double genome_divert(genome_t* self, genome_t* other);

void genome_show(genome_t self, genome_t* paths);

void genome_mutate(genome_t gen);

void genome_nmutate(genome_t gen);

void genome_smutate(genome_t gen);

void genome_translate(genome_t gen);

#endif
