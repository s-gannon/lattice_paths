#pragma once
#ifndef PATH_H
#define PATH_H

typedef struct {
	uint16_t m, n;
	int num_paths;
	path* paths;
} person;

void person_init(person* person, uint16_t m, uint16_t n, int num_paths);
float person_fitness(person* person, int k);
void person_show(person person);

#endif
