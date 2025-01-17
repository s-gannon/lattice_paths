""" Genetic program for Maths Research """
import random, winsound, numpy
from datetime import datetime
random.seed(getattr(datetime.now(), "microsecond"))
            
#generate a sequence depends on the values of m and n

class Sequence():
    def __init__(self, m, n):
        assert m >= n
        r=random.randint(0,1)
        self.terms = [[0,0,r]]
        m_count = 0
        n_count = 0

        for i in range(m+n-1):
            if r==1 and n_count<n:
                
                n_count += 1
                r2 = random.randint(0,1)
                self.terms.append([self.terms[i][0],self.terms[i][1]+1, r2])
                r= r2
            elif r==0 and m_count<m:
                m_count +=1
                r2 = random.randint(0,1)
                self.terms.append([self.terms[i][0]+1,self.terms[i][1], r2])
                r= r2
            elif r==1 and n_count==n:
                self.terms[i] = [self.terms[i][0],self.terms[i][1], 0]
                for j in range(i, m+n-1):
                    
                    self.terms.append([self.terms[j][0]+1,self.terms[j][1], 0])
                break
            elif r==0 and m_count==m:
                self.terms[i] = [self.terms[i][0],self.terms[i][1], 1]
                for j in range(i, m+n-1):
                    
                    self.terms.append([self.terms[j][0],self.terms[j][1]+1, 1])
                break
        if self.terms[-1][0] == m:
            self.terms[-1][2] = 1
        if self.terms[-1][1] == n:
            self.terms[-1][2] = 0
    def show(self):
        for term in self.terms:
            print(term[0],term[1], term[2], sep=" ", end="   ")
    def compare(self,sequence,k):
        check= 0
        for i in range(len(sequence.terms)):
            if sequence.terms[i] == self.terms[i]:#can make tis better someow
                check += 1
        if check >= k:
            return 0
        else:
            return 1

            
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
                    if self.sequences[i].terms[z] == self.sequences[j].terms[z]:
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
            r = self.fitness()[-1][random.randint(0,len(self.fitness()[-1])-1)][random.randint(0,1)]
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
        self.max_size = int(size/2)
        self.roulette_ready = False
        self.best_fitness = 0
        self.bfi = 0
        self.just_initialized = False

    def initialize(self):
        print("refilling")
        for z  in range(self.size):
            new_genome = Genome(self.num_genes,self.m,self.n,self.k)
            self.individuals.append(new_genome)
            f = new_genome.fitness()[0]
            self.fitnesses = numpy.append(self.fitnesses,f)#you might later want to know where equivalences occur though
            if f > self.best_fitness:
                self.best_fitness = f
                self.bfi = z
            if f == 9999:
                new_genome.show()
                winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
                return (len(self.individuals),self.c+1)
        self.just_initialized = True        
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
        print("battling")
        info_pool = 0.1
        if mode == "non_bias_random":
        #num_duels = int(duel_coef * len(population))
            l = len(self.individuals) # we cannot use this for indexes because the size of the population keeps changing, maybe copying to mating pool will be better
            #num_duels = random.randint(0, int(l/2))
            #for i in range(num_duels):
            while(len(self.individuals) > self.max_size):
                index_1 = random.randint(0, len(self.individuals)-1) #we subtract 1 bescause the randint() function includes the bounds
                index_2 = random.randint(0, len(self.individuals)-1)
                while index_1 == index_2:
                    index_2 = random.randint(0, len(self.individuals)-1)
                if self.fitnesses[index_1] < self.fitnesses[index_2]:
                    self.fitnesses = numpy.delete(self.fitnesses, index_1)
                    self.individuals.pop(index_1)
                #elif population[index_1].fitness()[0] > population[index_2].fitness()[0]:
                else:
                    self.fitnesses = numpy.delete(self.fitnesses, index_2)
                    self.individuals.pop(index_2)


        elif mode == "keep_fit":
            top_n = 10 
            self.bsort()
            #l = len(self.individuals)
            #num_duels = random.randint(0, int(l/2))
            #num_duels = 0.57
            #for i in range(int(num_duels*l)):
            while(len(self.individuals) > self.max_size):#not good! might get stuck in here due to "infor pool"
                index_1 = random.randint(0, len(self.individuals)-1) #we subtract 1 because the randint() function includes the bounds
                index_2 = random.randint(0, len(self.individuals)-1)
                while index_1 == index_2:
                    index_2 = random.randint(0, len(self.individuals)-1)
                if self.fitnesses[index_1] < self.fitnesses[index_2] and index_1 > top_n and index_1 < (len(self.individuals)-int(info_pool*len(self.individuals))):
                    self.fitnesses = numpy.delete(self.fitnesses, index_1)
                    self.individuals.pop(index_1)
                #elif population[index_1].fitness()[0] > population[index_2].fitness()[0]:
                elif self.fitnesses[index_1] > self.fitnesses[index_2] and index_2 > top_n and index_2 < (len(self.individuals)-int(info_pool*len(self.individuals))):
                    self.fitnesses = numpy.delete(self.fitnesses, index_2)
                    self.individuals.pop(index_2)
    def parent_pick(self, mode = "roulette"):
        assert len(self.fitnesses) == len(self.individuals)
        
        if mode == "roulette":
            if not self.roulette_ready:
                #increasin fitness of information pool
                #for fitness in self.fitnesses[-int(0.3*len(self.individuals)):]:
                    #fitness = 0.1
                                              
                
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
        mating_coef = 0.6
        self.just_initialized = False
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
                if a > self.best_fitness:
                    self.best_fitness = a
                    self.bfi = len(self.individuals) + len(self.children) -2#yes, minus 2 
                elif b > self.best_fitness:
                    self.bset_fitness = b
                    self.bfi = len(self.individuals) + len(self.children) -1
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
            """
            for i in self.individuals:
                if i.fitness()[0]==9999:
                    i.show()
                    return True
            """
            if self.best_fitness == 9999:
                assert self.individuals[self.bfi].fitness()[0] == 9999
                self.individuals[self.bfi].show()
                return True
            else:
                print(self.best_fitness)
        return False    
        
    def evolution(self,eons,mode):
        self.initialize()
        self.bsort()
        found = False
        for i in range(1,eons):
            if found == False:
                if not self.just_initialized:
                    self.battle("non_bias_random")
                self.mating(mode)
                found = self.check("speedy")
                print(i)
                #self.sorted = False not necessary, since sorted after check 
                
            else:
                print(i)
                print(len(self.individuals))
                break
            if (i)%10 == 0:
                self.initialize()
                self.sorted = False
                self.roulette_ready = False
        print(len(self.individuals))

def test(j,m,n,k,mode):
    world = Population(400,m,n,k)
    world.num_genes =j
    world.evolution(10000,mode)
        
 
                
            
            

