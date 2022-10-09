""" Genetic program for Maths Research """
import random, winsound, numpy
from datetime import datetime
random.seed(getattr(datetime.now(), "microsecond"))
class Term():
    def __init__(self, bit_1 = 0, bit_2=0, bit_3 = 0):
        self.bits = [bit_1, bit_2, random.randint(0,1)]
class Sequence():
    def __init__(self, m, n):
        assert m >= n
        self.terms = []
        for i in range(m+n):
            self.terms.append(Term())
            if i > 0:
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
            if sequence.terms[i].bits == self.terms[i].bits:#can make tis better someow
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
            for j in range(i+1,len(self.sequences)):
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
            return (9999, penalty_index)

        return (1/penalty, penalty_index)
                        
    def show(self):
        for sequence in self.sequences:
            sequence.show()
            print("\n")
    def mutate(self):
        #if random.randint(0, 37) % random.randint(2,3) == 0:
            #r = random.randint( 0, len(self.sequences) -1)
        if self.fitness()[-1]:
            r = self.fitness()[-1][0][0]
            self.sequences[r] = Sequence(self.m, self.n)
        return self
    
#raw evolution, will optimize later*

def softmax(x):
    return numpy.exp(x)/numpy.sum(numpy.exp(x))
class Population():
    def __init__(self,size, m, n, k): 
        self.individuals = []
        self.children = []
        assert m>0 and n>0 and m>=n
        self.m = m
        self.n = n
        self.k = k
        self.size = size
        self.c = 0
        self.fitnesses = numpy.array([])
        self.c_fitnesses = numpy.array([])
        self.r_fitnesses = numpy.array([])
        self.num_genes = 1
        self.sorted = False
        self.max_size = 1000
        self.roulette_ready = False

    def initialize(self):
        print("refilling")
        for z  in range(self.size):
            new_genome = Genome(self.num_genes,self.m,self.n,self.k)
            self.individuals.append(new_genome)
            self.fitnesses = numpy.append(self.fitnesses,new_genome.fitness()[0])#you might later want to know where equivalences occur though 
            if new_genome.fitness()[0] == 9999:
                new_genome.show()
                winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
                return (len(self.individuals),self.c+1)
    def bsort(self):
        #assert self.sorted == False
        assert len(self.individuals) == len(self.fitnesses)
        if self.sorted==False:
            print("sorting")
            l = len(self.fitnesses)
            for i in range(l):
                for j in range(l-i-1):
                    if self.fitnesses[j] < self.fitnesses[j+1]:
                        temp = self.individuals[j]
                        temp1 = self.fitnesses[j]
                        self.individuals[j] = self.individuals[j+1]
                        self.fitnesses[j] = self.fitnesses[j+1]
                        self.individuals[j+1] = temp
                        self.fitnesses[j+1] = temp1
            self.sorted = True
        
    def battle(self, mode = "keep_fit"):
        if mode == "non_bias_random":
        #num_duels = int(duel_coef * len(population))
            l = len(self.individuals) # we cannot use this for indexes because the size of the population keeps changing, maybe copying to mating pool will be better
            num_duels = random.randint(0, int(l/2))
            #for i in range(num_duels):
            while(len(self.individuals) > self.max_size):
                index_1 = random.randint(0, len(self.individuals)-1) #we subtract 1 because the randint() function includes the bounds
                index_2 = random.randint(0, len(self.individuals)-1)
                while index_1 == index_2:
                    index_2 = random.randint(0, len(self.individuals)-1)
                if self.individuals[index_1].fitness()[0] < self.individuals[index_2].fitness()[0]:
                    self.fitnesses = numpy.delete(self.fitnesses, index_1)
                    self.individuals.pop(index_1)
                #elif population[index_1].fitness()[0] > population[index_2].fitness()[0]:
                else:
                    self.fitnesses = numpy.delete(self.fitnesses, index_2)
                    self.individuals.pop(index_2)

        elif mode == "keep_fit":
            top_n = 10 
            ##self.bsort()
            l = len(self.individuals)
            #num_duels = random.randint(0, int(l/2))
            num_duels = 0.57
            #for i in range(int(num_duels*l)):
            while(len(self.individuals) > self.max_size):
                index_1 = random.randint(0, len(self.individuals)-1) #we subtract 1 because the randint() function includes the bounds
                index_2 = random.randint(0, len(self.individuals)-1)
                while index_1 == index_2:
                    index_2 = random.randint(0, len(self.individuals)-1)
                if self.individuals[index_1].fitness()[0] < self.individuals[index_2].fitness()[0] and index_1 > top_n and index_1 < (len(self.individuals)-int(0.3*len(self.individuals))):
                    self.fitnesses = numpy.delete(self.fitnesses, index_1)
                    self.individuals.pop(index_1)
                #elif population[index_1].fitness()[0] > population[index_2].fitness()[0]:
                elif index_2 > top_n and index_2 < (len(self.individuals)-int(0.3*len(self.individuals))):
                    self.fitnesses = numpy.delete(self.fitnesses, index_2)
                    self.individuals.pop(index_2)
    def parent_pick(self, mode = "roulette"):
        assert len(self.fitnesses) == len(self.individuals)
        
        if mode == "roulette":
            if not self.roulette_ready:
                #increasin fitness of information pool
                for fitness in self.fitnesses[-int(0.3*len(self.individuals)):]:
                    fitness = 0.1
                                              
                
                    #if not self.sorted:
                        #self.bsort()
                self.bsort()
                    #self.e_fitnesses = softmax(self.fitnesses)
                if numpy.sum(self.r_fitnesses) != 1:
                    self.r_fitnesses = self.fitnesses/numpy.sum(self.fitnesses)
                    sumf = 0
                    for i in range(len(self.r_fitnesses)):
                        self.r_fitnesses[i] = sumf + self.r_fitnesses[i]
                        sumf = self.r_fitnesses[i]
                self.roulette_ready = True                 
            rand1 = numpy.random.random(1)
            rand2 = numpy.random.random(1)
            parent_1_index = 0
            parent_2_index = 1
            for i in range(len(self.r_fitnesses)):
                if rand1 <= self.r_fitnesses[i]:
                    parent_1_index = i
                    break
            for i in range(len(self.r_fitnesses)):
                if rand2 <= self.r_fitnesses[i]:
                    parent_2_index = i
                    break
            #self.r_fitnesses = numpy.array([])   
            return (parent_1_index, parent_2_index)

        elif mode == "random_random":
            parent_1_index = random.randint(0, len(self.individuals)-1)
            parent_2_index = random.randint(0, len(self.individuals)-1)
            while parent_1_index == parent_2_index:
                parent_2_index = random.randint(0, len(self.individuals)-1)
            return (parent_1_index, parent_2_index)
            
            
             
    def mating(self, mode = "random_random"):
        #mating_coef = ra'ndom.random()
        print("mating")
        mating_coef = 0.555
        l = len(self.individuals)
        for j in range(int(mating_coef * l)):
            co_coef = random.random()
            parent_1_index, parent_2_index = self.parent_pick(mode)
            if parent_1_index != parent_2_index:

                encoding_part_1 = random.randint(1,2) #first sequences of genes of child 1 come from parent 1

                new_child_1 = Genome(self.num_genes,self.m,self.n,self.k)
                new_child_2 = Genome(self.num_genes, self.m,self.n,self.k)
                if encoding_part_1 == 1:
                    for s in range(int(self.num_genes * co_coef)):
                           
                        new_child_1.sequences[s] = self.individuals[parent_1_index].sequences[s]
                        new_child_2.sequences[s] = self.individuals[parent_2_index].sequences[s]
                        
                    for s in range(int(self.num_genes*co_coef), self.num_genes):
                        
                        new_child_1.sequences[s] = self.individuals[parent_2_index].sequences[s]
                        new_child_2.sequences[s] = self.individuals[parent_1_index].sequences[s]
                        
                else:
                    for s in range(int(self.num_genes*co_coef), self.num_genes):
                           
                        new_child_1.sequences[s] = self.individuals[parent_1_index].sequences[s]
                        new_child_2.sequences[s] = self.individuals[parent_2_index].sequences[s]
                        
                    for s in range(int(self.num_genes * co_coef)):

                        new_child_1.sequences[s] = self.individuals[parent_2_index].sequences[s]
                        new_child_2.sequences[s] = self.individuals[parent_1_index].sequences[s]
                        
                new_child_2= new_child_2.mutate()
                self.children.append(new_child_1)
                self.children.append(new_child_2)
                a =new_child_1.fitness()[0]
                b=new_child_2.fitness()[0]
                self.c_fitnesses =numpy.append(self.c_fitnesses, a)
                self.c_fitnesses = numpy.append(self.c_fitnesses, b) #a before b(in order in which individuals were appended)!

        self.individuals+=self.children
        self.sorted = False
        self.children = []
        self.fitnesses = numpy.concatenate((self.fitnesses, self.c_fitnesses))
        self.c_fitnesses = numpy.array([])
        self.r_fitnesses = numpy.array([])
        self.roulette_ready = False

            

            
            
    def check(self, mode):
        print("checking")
        if mode == "roulette":
            
            self.bsort()
            for fitness in self.fitnesses[:10]:
                #individual.show()
                print(fitness)
            if self.individuals[0].fitness()[0] == 9999:
                print(len(self.individuals))
                self.individuals[0].show()
                winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
                
                return True
            else:
                return False
        else:
            for i in self.individuals:
                if i.fitness()[0]==9999:
                    i.show()
                    return True
        return False    
        
    def evolution(self,eons,mode):
        self.initialize()
        self.bsort()
        found = False
        for i in range(eons):
            if found == False:
                self.battle()
                self.mating(mode)
                found = self.check(mode)
                print(i)
                #self.sorted = False not necessary, since sorted after check 
                
            else:
                print(i)
                print(len(self.individuals))
                break
            if i%10 == 0:
                self.initialize()
                self.sorted = False
                self.roulette_ready = False
        print(len(self.individuals))

def test(j,m,n,k,mode):
    world = Population(2000,m,n,k)
    world.num_genes =j
    world.evolution(10000,mode)
        

    
