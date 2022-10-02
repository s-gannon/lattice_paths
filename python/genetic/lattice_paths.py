#!/bin/python
""" Genetic program for Maths Research """
import random
from datetime import datetime
random.seed(getattr(datetime.now(), "microsecond"))
class Term():
    def __init__(self, bit_1 = 0, bit_2=0, bit_3 = 0):
        self.bits = [bit_1, bit_2, random.randint(0,1)]
class Sequence():
    def __init__(self, m, n):
        assert m >= n   #I think we should be able to create any m by n lattice, but I do like the idea of the assert before the function call
        self.terms = []
        for i in range(m+n):
            self.terms.append(Term())
            if i > 0:   #I understand having this check to be pedantic, but technically unnecessary
                if self.terms[i-1].bits[2] == 0 and self.terms[i-1].bits[0] < m:
                    self.terms[i].bits[1] = self.terms[i-1].bits[1]
                    self.terms[i].bits[0] = self.terms[i-1].bits[0] + 1
                elif self.terms[i-1].bits[2]==0 and self.terms[i-1].bits[0] == m:
                    self.terms[i-1].bits[2] = 1
                    self.terms[i].bits[2] =1
                    self.terms[i].bits[1] = self.terms[i-1].bits[1] + 1
                    self.terms[i].bits[0] = self.terms[i-1].bits[0]
                elif self.terms[i-1].bits[2]== 1 and self.terms[i-1].bits[1] < n:
                    self.terms[i].bits[0] = self.terms[i-1].bits[0]
                    self.terms[i].bits[1] = self.terms[i-1].bits[1] + 1
                elif self.terms[i-1].bits[2] == 1 and self.terms[i-1].bits[1] == n:
                    self.terms[i-1].bits[2] = 0
                    self.terms[i].bits[2] = 0
                    self.terms[i].bits[0] = self.terms[i-1].bits[0] + 1
                    self.terms[i].bits[1] = self.terms[i-1].bits[1]
            if i == (m+n)-1:
                if m==n:
                    if self.terms[i].bits[1] > self.terms[i].bits[0]:
                        self.terms[i].bits[2] = 0
                    else:
                        self.terms[i].bits[2] = 1
                elif self.terms[i].bits[1] == n:
                    self.terms[i].bits[2] = 0
                elif self.terms[i].bits[0] == m:
                    self.terms[i].bits[2] = 1
    def show(self):
        for term in self.terms:
            print(term.bits[0], term.bits[1], term.bits[2], sep=" ", end="   ")
    def compare(self,sequence,k):
        check= 0
        for i in range(len(sequence.terms)):
            if sequence.terms[i].bits == self.terms[i].bits:
                check += 1
        if check >= k:
            return 0
        else:
            return 1

#generate a sequence depends on the values of m and n

class Genome():
    def __init__(self, num_sequences, m, n, k):
        self.sequences = []
        self.m = m
        self.n = n
        self.k = k
        for i in range(num_sequences):
            self.sequences.append(Sequence(self.m, self.n))
    def fitness(self):
        penalty = 0
        check =0
        penalty_index = []

        for i in range(len(self.sequences)):
            for j in range(i+1,len(self.sequences)):    #this is at the very least making this an n^2 time complexity
                #if i is not j:
                for z in range(self.m + self.n):
                    if self.sequences[i].terms[z].bits == self.sequences[j].terms[z].bits:
                        check += 1
                if check >= self.k:
                    penalty += 1
                    penalty_index.append([i,j])
                    check = 0
                else:
                    check = 0
        if penalty ==0:
            return (9999, "No-penalty")

        return (1/penalty, penalty_index)
    def show(self):
        for sequence in self.sequences:
            sequence.show()
            print("\n")

#raw evolution, will optimize later*

def evolution(num_genes, m, n, k):
    population = []
    population_fitness = 0
    generation_fitnesses = []
    eons = 6000
    Z = 500
    duel_coef = 0.53
    co_coef = 0.8 #percentage gene exchange per crossover
    num_mating_coef = 0.535 #percentage of parents crossing over
    c=0
    s_co_coef = .7
    p_pl = 0
    nnl = 0
    for z  in range(Z):
        new_genome = Genome(num_genes,m,n,k)
        population.append(new_genome)
        if new_genome.fitness()[0] == 9999:
            new_genome.show()
            return (len(population),c+1)
    for e in range(1, eons):
        c+=1
        for genome in population:
            if genome.fitness()[0] == 9999:
                genome.show()
                return (len(population),c+1)


        #random duels
        num_duels = int(duel_coef * len(population))
        for i in range(num_duels):
            index_1 = random.randint(0, len(population)-1) #we subtract 1 because the randint() function includes the bounds
            index_2 = random.randint(0, len(population)-1)
            while index_1 == index_2:
                index_2 = random.randint(0, len(population)-1)
            if population[index_1].fitness()[0] < population[index_2].fitness()[0]:

                population.pop(index_1)
            elif population[index_1].fitness()[0] > population[index_2].fitness()[0]:
                population.pop(index_2)
            else:
                population.pop(index_2)
        p_pl = len(population)
        #cross-over genes
        #num_co_genes = co_coef * num_genes
        for j in range(int(num_mating_coef * len(population))):
            parent_1_index = random.randint(0, len(population)-1)
            parent_2_index = random.randint(0, len(population)-1)
            while parent_1_index == parent_2_index:
                parent_2_index = random.randint(0, len(population)-1)
            if parent_1_index != parent_2_index:

                encoding_part_1 = random.randint(1,2)
                encoding_part_2 = random.randint(1,2)
                #len_encoding_seq_1 =
                while encoding_part_2 == encoding_part_1:
                    encoding_part_2 = random.randint(1,2)
                new_child_1 = Genome(num_genes,m,n,k)
                prsi_list1 = []
                prsi_list2 = []
                if encoding_part_1 == 1:
                    for s in range(int(num_genes * co_coef)):
                        p_r_s_i = random.randint(0, num_genes-1)#parent random sequence index
                        while p_r_s_i in prsi_list1:
                            p_r_s_i = random.randint(0, num_genes-1)
                        prsi_list1.append(p_r_s_i)
                        new_child_1.sequences[s] = population[parent_1_index].sequences[p_r_s_i]
                    prsi_list1 = [] #test_in
                if encoding_part_1 == 2:
                    for s in range(int(num_genes*co_coef), int(num_genes)):
                        p_r_s_i = random.randint(0, num_genes-1)
                        while p_r_s_i in prsi_list1:
                            p_r_s_i = random.randint(0, num_genes-1)
                        prsi_list1.append(p_r_s_i)
                        new_child_1.sequences[s] = population[parent_1_index].sequences[p_r_s_i]
                    prsi_list1 = [] #test_in
                if encoding_part_2 == 1:
                    for s in range(int(num_genes * co_coef)):
                        p_r_s_i = random.randint(0, num_genes-1)
                        while p_r_s_i in prsi_list1:
                            p_r_s_i = random.randint(0, num_genes-1)
                        prsi_list1.append(p_r_s_i)
                        new_child_1.sequences[s] = population[parent_2_index].sequences[p_r_s_i]
                    prsi_list1 = [] #test_in
                if encoding_part_2 == 2:
                    for s in range(int(num_genes*co_coef), int(num_genes)):
                        p_r_s_i = random.randint(0, num_genes-1)
                        while p_r_s_i in prsi_list1:
                            p_r_s_i = random.randint(0, num_genes-1)
                        prsi_list1.append(p_r_s_i)
                        new_child_1.sequences[s] = population[parent_2_index].sequences[p_r_s_i]
                    prsi_list1 = [] #test_in , not needed here in fact since it is the last *if*
                #mutation
                if e%int(1) == 0:
                    r = random.randint(0, num_genes-1)
                    new_child_1.sequences[r] = Sequence(m,n)

                population.append(new_child_1)

                new_child_2 = Genome(num_genes, m,n,k)
                if encoding_part_1 == 2:
                    for s in range(int(num_genes*co_coef)):
                        p_r_s_i = random.randint(0, num_genes-1)
                        while p_r_s_i in prsi_list2:
                            p_r_s_i = random.randint(0, num_genes-1)
                        prsi_list2.append(p_r_s_i)
                        new_child_2.sequences[s] = population[parent_1_index].sequences[p_r_s_i]
                    prsi_list2 = [] #test_in
                if encoding_part_1==1:
                    for s in range(int(num_genes*co_coef), int(num_genes)):
                        p_r_s_i = random.randint(0, num_genes-1)
                        while p_r_s_i in prsi_list2:
                            p_r_s_i = random.randint(0, num_genes-1)
                        prsi_list2.append(p_r_s_i)
                        new_child_2.sequences[s] = population[parent_1_index].sequences[p_r_s_i]
                    prsi_list2 = [] #test_in
                if encoding_part_2 == 2:
                    for s in range(int(num_genes*co_coef)):
                        p_r_s_i = random.randint(0, num_genes-1)
                        while p_r_s_i in prsi_list2:
                            p_r_s_i = random.randint(0, num_genes-1)
                        prsi_list2.append(p_r_s_i)
                        new_child_2.sequences[s] = population[parent_2_index].sequences[p_r_s_i]
                    prsi_list2 = [] #test_in
                if encoding_part_2==1:
                    for s in range(int(num_genes*co_coef), int(num_genes)):
                        p_r_s_i = random.randint(0, num_genes-1)
                        while p_r_s_i in prsi_list2:
                            p_r_s_i = random.randint(0, num_genes-1)
                        prsi_list2.append(p_r_s_i)
                        new_child_2.sequences[s] = population[parent_2_index].sequences[p_r_s_i]
                    prsi_list2 = [] #test_in
                #mutation
                if e%int(5) == 0:
                    r = random.randint(0, num_genes-1)
                    new_child_1.sequences[r] = Sequence(m,n)
                if e%int(9) == 0:
                    r_1 = random.randint(0, num_genes-1)
                    r_2 = random.randint(0, num_genes-1)
                    new_child_2.sequences[r_1] = Sequence(m,n)
                    new_child_2.sequences[r_1] = Sequence(m,n)
                population.append(new_child_2)
        nnl = len(population)
        if e % int(eons*0.04) == 0:
            print(e)
            for i in range(len(population)):
                for j in range(len(population)-i-1):
                    if population[j].fitness()[0] <population[j+1].fitness()[0]:
                        temp = population[j]
                        population[j] = population[j+1]
                        population[j+1] = temp
            print(population[0].fitness())
            for i in range(1,21):
                for j in range(num_genes):
                    d_check = 0
                    for z in range(num_genes):

                        if population[i].sequences[j].compare(population[0].sequences[z], k)==1:
                            d_check += 1
                    if z == num_genes -1  and d_check <=(int(0.1*num_genes)+1):
                        #repetitions is not empty since the fittest guy would have been printed already
                        repetitions =population[0].fitness()[-1]
                        rando = random.randint(len(repetitions)-1)
                        rando_2 = random.randint(0,1)
                        swap_index = repetitions[rando][rando_2]
                        population[0].sequences[swap_index] = population[i].sequences[j]
            for i in range(-20,0):
                for j in range(num_genes):
                    d_check = 0
                    for z in range(num_genes):

                        if population[i].sequences[j].compare(population[0].sequences[z], k)==1:
                            d_check += 1
                    if z == num_genes -1  and d_check <=int(0.1*num_genes)+1:
                        repetitions =population[0].fitness()[-1]
                        rando = random.randint(len(repetitions)-1)
                        rando_2 = random.randint(0,1)
                        swap_index = repetitions[rando][rando_2]
                        population[0].sequences[swap_index] = population[i].sequences[j]


            for j in range(int(num_mating_coef * len(population)*0.5)):
                parent_1_index = random.randint(0, int(len(population)*0.2))
                parent_2_index = random.randint(0, int(len(population)*0.2))
                while parent_1_index == parent_2_index:
                    parent_2_index = random.randint(0, int(len(population)*0.2)-1)
                if parent_1_index != parent_2_index:

                    encoding_part_1 = random.randint(1,2)
                    encoding_part_2 = random.randint(1,2)
                    #len_encoding_seq_1 =
                    while encoding_part_2 == encoding_part_1:
                        encoding_part_2 = random.randint(1,2)
                    new_child_1 = Genome(num_genes,m,n,k)
                    prsi_list1 = []
                    prsi_list2 = []
                    if encoding_part_1 == 1:
                        for s in range(int(num_genes * s_co_coef)):
                            p_r_s_i = random.randint(0, num_genes-1)#parent random sequence index
                            while p_r_s_i in prsi_list1:
                                p_r_s_i = random.randint(0, num_genes-1)
                            prsi_list1.append(p_r_s_i)
                            new_child_1.sequences[s] = population[parent_1_index].sequences[p_r_s_i]
                        prsi_list1 = [] #test_in
                    if encoding_part_1 == 2:
                        for s in range(int(num_genes*s_co_coef), int(num_genes)):
                            p_r_s_i = random.randint(0, num_genes-1)
                            while p_r_s_i in prsi_list1:
                                p_r_s_i = random.randint(0, num_genes-1)
                            prsi_list1.append(p_r_s_i)
                            new_child_1.sequences[s] = population[parent_1_index].sequences[p_r_s_i]
                        prsi_list1 = [] #test_in
                    if encoding_part_2 == 1:
                        for s in range(int(num_genes * s_co_coef)):
                            p_r_s_i = random.randint(0, num_genes-1)
                            while p_r_s_i in prsi_list1:
                                p_r_s_i = random.randint(0, num_genes-1)
                            prsi_list1.append(p_r_s_i)
                            new_child_1.sequences[s] = population[parent_2_index].sequences[p_r_s_i]
                        prsi_list1 = [] #test_in
                    if encoding_part_2 == 2:
                        for s in range(int(num_genes*s_co_coef), int(num_genes)):
                            p_r_s_i = random.randint(0, num_genes-1)
                            while p_r_s_i in prsi_list1:
                                p_r_s_i = random.randint(0, num_genes-1)
                            prsi_list1.append(p_r_s_i)
                            new_child_1.sequences[s] = population[parent_2_index].sequences[p_r_s_i]
                        prsi_list1 = [] #test_in , not needed here in fact since it is the last *if*
                    #mutation
                    if e%int(1) == 0:
                        r = random.randint(0, num_genes-1)
                        new_child_1.sequences[r] = Sequence(m,n)

                    population.append(new_child_1)

                    new_child_2 = Genome(num_genes, m,n,k)

                    if encoding_part_1 == 2:
                        for s in range(int(num_genes*s_co_coef)):
                            p_r_s_i = random.randint(0, num_genes-1)
                            while p_r_s_i in prsi_list2:
                                p_r_s_i = random.randint(0, num_genes-1)
                            prsi_list2.append(p_r_s_i)
                            new_child_2.sequences[s] = population[parent_1_index].sequences[p_r_s_i]
                        prsi_list2 = [] #test_in
                    if encoding_part_1==1:
                        for s in range(int(num_genes*s_co_coef), int(num_genes)):
                            p_r_s_i = random.randint(0, num_genes-1)
                            while p_r_s_i in prsi_list2:
                                p_r_s_i = random.randint(0, num_genes-1)
                            prsi_list2.append(p_r_s_i)
                            new_child_2.sequences[s] = population[parent_1_index].sequences[p_r_s_i]
                        prsi_list2 = [] #test_in
                    if encoding_part_2 == 2:
                        for s in range(int(num_genes*s_co_coef)):
                            p_r_s_i = random.randint(0, num_genes-1)
                            while p_r_s_i in prsi_list2:
                                p_r_s_i = random.randint(0, num_genes-1)
                            prsi_list2.append(p_r_s_i)
                            new_child_2.sequences[s] = population[parent_2_index].sequences[p_r_s_i]
                        prsi_list2 = [] #test_in
                    if encoding_part_2==1:
                        for s in range(int(num_genes*s_co_coef), int(num_genes)):
                            p_r_s_i = random.randint(0, num_genes-1)
                            while p_r_s_i in prsi_list2:
                                p_r_s_i = random.randint(0, num_genes-1)
                            prsi_list2.append(p_r_s_i)
                            new_child_2.sequences[s] = population[parent_2_index].sequences[p_r_s_i]
                        prsi_list2 = [] #test_in
                    #mutation
                    if (e*237)%int(15) == 0:
                        r_1 = random.randint(0, num_genes-1)
                        r_2 = random.randint(0, num_genes-1)
                        new_child_2.sequences[r_1] = Sequence(m,n)
                        new_child_2.sequences[r_2] = Sequence(m,n)
                    population.append(new_child_2)
            for z  in range(int(Z*0.3)):
                new_genome = Genome(num_genes,m,n,k)
                population.append(new_genome)
                if new_genome.fitness()[0] == 9999:
                    new_genome.show()
                    return (len(population),c+1)
    return (len(population),c+1)
