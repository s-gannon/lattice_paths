#!/usr/bin/python3
""" Genetic program for Maths Research:finding K distinct paths for an m by n lattice, m>n """
import random, os, openpyxl
from sys import argv
from datetime import datetime
random.seed(getattr(datetime.now(), "microsecond"))
        
#generate a sequence depends on the values of m and n

class Sequence():
    def __init__(self, m, n, empty=False):
        assert m >= n
        r=random.randint(0,1)
        self.terms = [[0,0,r]]
        m_count = 0
        n_count = 0
        if not empty:
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
        else:
            for i in range(m+n-1):
                self.terms.append([0,0,0])
    def show(self):
        for term in self.terms:
            print(term[0],term[1], term[2], sep=" ", end="   ")
    def compare(self,sequence,k):
        assert len(self.terms) == len(sequence.terms)
        check= 0
        for i in range(len(self.terms)):
            if sequence.terms[i] == self.terms[i]:#can make tis better someow
                check += 1
        if check >= k:
            return 0
        else:
            return 1
    def ispoison(self,sequence):
        for i in range(len(self.terms)):
            if sequence.terms[i] != self.terms[i]:
                return 0

        return 1



def translate(patA,to_lan):
    if to_lan == "to_O":
        num_0 =0
        num_1 =0
        for i in patA:
            if i:
                num_1 += 1
            else:
                num_0 += 1
        assert num_0 >= num_1        
        patO = Sequence(num_0, num_1)
        for i in range(len(patO.terms)):
            if i!= len(patA)-1:
                if patA[i] == 0:
                    patO.terms[i][2] = 0
                    patO.terms[i+1][0] = patO.terms[i][0] + 1
                    patO.terms[i+1][1] = patO.terms[i][1]
                else:
                    patO.terms[i][2] = 1
                    patO.terms[i+1][0] = patO.terms[i][0]
                    patO.terms[i+1][1] = patO.terms[i][1] +1
            else:
                if patA[i] == 0:
                    patO.terms[i][2] = 0
                else:
                    patO.terms[i][2] = 1
                    
        return patO
    elif to_lan == "to_A":
        patO = []
        for term in patA.terms:
            patO.append(term[2])
        return patO    
                        
class Genome():
    def __init__(self, num_sequences, m, n, k, empty=False):
        self.sequences = []
        self.m = m
        self.n = n
        self.k = k
        #self.poison()
        if not empty:
            for i in range(num_sequences):
                new_seq = Sequence(self.m, self.n)
                #while new_seq.ispoison(self.poison1) or new_seq.ispoison(self.poison2):
                    #new_seq = Sequence(self.m, self.n)
                self.sequences.append(new_seq)
        else:
            for i in range(num_sequences):
                new_seq = Sequence(self.m, self.n, True)
                self.sequences.append(new_seq)
            
                 

    def fitness(self):
        penalty = 0
        #check =0
        penalty_index = []

        for i in range(len(self.sequences)):
            for j in range(i+1,len(self.sequences)):
                #if i is not j:
                #for z in range(self.m + self.n):
                    #if self.sequences[i].terms[z] == self.sequences[j].terms[z]:
                        #check += 1
                xo = self.sequences[i].compare(self.sequences[j], self.k)
                if xo == 0:
                    #check = x[1]
                    penalty += 1
                    penalty_index.append([i,j])

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

    def translate(self):
        translated = []
        for sequence in self.sequences:
            translated.append(translate(sequence,"to_A"))

        return translated    

    def poison(self):
        patA = []
        patB = []
        if self.k<=self.m:
            for i in range(self.k):
                patA.append(0)
            for i in range(self.n):
                patA.append(1)
                #patB.append(0)
            for i in range(self.m - self.k):
                patA.append(0)
        else:
            for s in range(self.m+self.n):
                patA.append(1)
        if self.k<=self.n:        
            for i in range(self.k):
                patB.append(1)
            for i in range(self.m):
                patB.append(0)
                #patB.append(0)
            for i in range(self.n - self.k):
                patB.append(1)
        else:
            for s in range(self.m+self.n):
                patB.append(1)
                
        self.poison2 = translate(patB, "to_O") 
        self.poison1 = translate(patA, "to_O")                
    
#raw evolution, will optimize later*

def softmax(x):
    return numpy.exp(x)/numpy.sum(numpy.exp(x))
def sume(x):
    sume = 0
    for i in x:
        sume+=i
    return sume       
class Population():
    def __init__(self,size, m, n, k,create_paths = True): 
        self.individuals = []
        self.children = []
        assert m>0 and n>0 and m>=n
        self.m = m
        self.n = n
        self.k = k
        self.size = size
        self.c = 0
        self.fitnesses = []
        self.c_fitnesses = []
        self.r_fitnesses = []
        self.num_genes = 1
        self.sorted = False
        self.max_size = int(size/2)
        self.roulette_ready = False
        self.best_fitness = 0
        self.bfi = 0
        self.just_initialized = False
        #self.paths = wdw(m,n)
        if create_paths:
            
            self.paths = wdw(m,n)
            self.l = len(self.paths)

    def initialize(self):
        print("refilling")
        self.just_initialized = True
        l = len(self.paths)
        i = 0
        for r in range(50):
            new_genome = Genome(self.num_genes,self.m,self.n,self.k, True)
            for s in range(self.num_genes):
                new_genome.sequences[s].terms = self.paths[i%l]
                i+=1
            self.individuals.append(new_genome)
            f = new_genome.fitness()[0]
             
            self.fitnesses.append(f)#you might later want to know where equivalences occur though
            if f > self.best_fitness:
                self.best_fitness = f
                self.bfi = len(self.individuals) -1
                self.bsort()
            if f == 9999:
                new_genome.show()
                #winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
                self.bsort()
                return True
            
            
            
        for z  in range(self.size):
            new_genome = Genome(self.num_genes,self.m,self.n,self.k)
            self.individuals.append(new_genome)
            f = new_genome.fitness()[0]
            self.fitnesses.append(f)#you might later want to know where equivalences occur though
            if f > self.best_fitness:
                self.best_fitness = f
                self.bfi = len(self.individuals) -1
                self.bsort()
            if f == 9999:
                new_genome.show()
               # winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
                self.bsort()
                return True
        self.bsort()
        return False    
               
    def bsort(self):
        #assert self.sorted == False
        assert len(self.individuals) == len(self.fitnesses)
        """
        print("before sorting")
        for i in range(len(self.individuals)):
            #print(self.fitnesses[i], self.individuals[i].fitness()[0] )
            assert self.fitnesses[i] == self.individuals[i].fitness()[0]
        """    
        if self.sorted==False:
            print("sorting")
            l = len(self.fitnesses)
            for i in range(l):
                swapped = False
                for j in range(0,l-i-1):
                    if self.fitnesses[j] < self.fitnesses[j+1]:
                        temp = self.individuals[j]
                        temp1 = self.fitnesses[j]
                        self.individuals[j] = self.individuals[j+1]
                        self.fitnesses[j] = self.fitnesses[j+1]
                        self.individuals[j+1] = temp
                        self.fitnesses[j+1] = temp1
                        swapped = True
                
                if swapped == False:
                    break
            self.bfi = 0            
            self.sorted = True
        """    
        print("after sorting")
        q = len(self.fitnesses)
        for i in range(q):
            
            assert self.fitnesses[i] == self.individuals[i].fitness()[0]        
        """  
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
                    self.fitnesses.pop(index_1)
                    self.individuals.pop(index_1)
                #elif population[index_1].fitness()[0] > population[index_2].fitness()[0]:
                else:
                    self.fitnesses.pop(index_2)
                    self.individuals.pop(index_2)


        elif mode == "keep_fit":
            top_n = 10 
            self.bsort()
            ###note to myself, new children are at the end of the population so needless to sort for info pool
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
                    self.fitnesses.pop(index_1)
                    self.individuals.pop(index_1)
                #elif population[index_1].fitness()[0] > population[index_2].fitness()[0]:
                elif self.fitnesses[index_1] > self.fitnesses[index_2] and index_2 > top_n and index_2 < (len(self.individuals)-int(info_pool*len(self.individuals))):
                    self.fitnesses.pop(index_1)
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
                if sume(self.r_fitnesses) != 1:
                    self.r_fitnesses = []
                    sum_fitnesses =sume(self.fitnesses)
                    for x in self.fitnesses:
                        self.r_fitnesses.append(x/sum_fitnesses)

                    sumf = 0
                    for i in range(len(self.r_fitnesses)):
                        self.r_fitnesses[i] = sumf + self.r_fitnesses[i]
                        sumf = self.r_fitnesses[i]
                self.roulette_ready = True
                 
            rand1 = int.from_bytes(os.urandom(8),byteorder="big")/((1<<64)-1)
            rand2 = int.from_bytes(os.urandom(8),byteorder="big")/((1<<64)-1)
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
        mating_coef = 0.7
        self.just_initialized = False 
        l = len(self.individuals)
        for j in range(int(mating_coef * l)):
            co_coef = int.from_bytes(os.urandom(8),byteorder="big")/((1<<64)-1)
            parent_1_index, parent_2_index = self.parent_pick(mode)
            if parent_1_index != parent_2_index:

                encoding_part_1 = random.randint(1,2) #first sequences of genes of child 1 come from parent 1

                new_child_1 = Genome(self.num_genes,self.m,self.n,self.k)
                new_child_2 = Genome(self.num_genes, self.m,self.n,self.k)
                if encoding_part_1 == 1:#you can reduce this to two for loops ... indexin usin num_genes-s maybe
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
                self.c_fitnesses.append(a)
                self.c_fitnesses.append(b) #a before b(in order in which individuals were appended)!
                if a > self.best_fitness:
                    self.best_fitness = a
                    self.bfi = len(self.individuals) + len(self.children) -2#yes, minus 2 since a is appended before b
                elif b > self.best_fitness:
                    self.best_fitness = b
                    self.bfi = len(self.individuals) + len(self.children) -1
        """ 
        assert len(self.c_fitnesses) == len(self.children)
        sss =0
        for i in range(len(self.c_fitnesses)):
            
            #print(self.children[i].fitness()[0],self.c_fitnesses[i])
            assert self.children[i].fitness()[0] == self.c_fitnesses[i]
            if self.children[i].fitness()[0] == self.c_fitnesses[i]:
                sss+=1
        print(sss, len(self.c_fitnesses))
        #assert True == False
        """ 
        self.individuals+=self.children
        self.sorted = False
        self.children = []
        self.fitnesses += self.c_fitnesses
        self.c_fitnesses = []
        self.r_fitnesses = []
        self.roulette_ready = False
        """
        assert len(self.fitnesses) == len(self.individuals)
        sss =0
        for i in range(len(self.fitnesses)):
            
            #print(self.individuals[i].fitness()[0],self.fitnesses[i])
            #assert self.individuals[i].fitness()[0] == self.fitnesses[i]
            if self.individuals[i].fitness()[0] == self.fitnesses[i]:
                sss+=1
        print(sss, len(self.fitnesses))
        #assert True == False        
        """
            

            
            
    def check(self, mode):
        print("checking")
        #self.bsort()
        if mode == "roulette" or mode=="random_random":
            
            self.bsort()
            for fitness in self.fitnesses[:10]:
                #individual.show()
                print(fitness)
            if self.individuals[0].fitness()[0] == 9999:
                print(len(self.individuals))
                self.individuals[0].show()
               # winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
                
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
                #winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
                #self.bsort()
                return True
            else:
                print("({},{},{},{}) \n".format(self.num_genes,self.m,self.n,self.k))
                print(self.bfi,self.individuals[self.bfi].fitness()[0],self.best_fitness)
                assert self.individuals[self.bfi].fitness()[0] == self.best_fitness
                print(self.best_fitness)
        return False    
        
    def evolution(self,eons,mode,mitigate_convergence):
        
        #self.bsort()
        #found = False
        found = self.initialize()
        for i in range(1,eons):
            print(i)
            if found == False:
                if self.just_initialized==False:
                    self.battle("non_bias_random")
                    self.mating(mode)
                else:
                    self.mating("random_random")
                found = self.check("speedy")
                
                #self.sorted = False not necessary, since sorted after check
                #self.sorted = False #yes, because not sorted after speedy check; IN fact not needed since not sorted = false after matin
                
            else:
                
                
                print("self.bfi = ", self.bfi)
                print("solutions = {},m = {}, n = {}, k = {}".format(self.num_genes,self.m,self.n, self.k))
                print("size of population", len(self.individuals), "best fitness", self.best_fitness)
                return self.individuals[self.bfi]
                
            if (i)%10 == 0:
                found = self.initialize()
                self.sorted = False
                self.roulette_ready = False
 
        print("solutions = {},m = {}, n = {}, k = {}".format(self.num_genes,self.m,self.n, self.k))        
        print("size of sub-population", len(self.individuals), "best fitness", self.best_fitness)
        print("bfi, size of pop",self.bfi, len(self.individuals))
        return self.individuals[self.bfi]
        

def test(j,m,n,k,mode, mitigate_convergence):
    world = Population(1000,m,n,k)
    world.num_genes =j
    best = world.evolution(10000,mode, mitigate_convergence)
    return best
       
def run(m,n,k,mode,old_world=0):
    filename = "lattice_table_" + str(n) + '.xlsx'
    try:
        wb = openpyxl.load_workbook(filename)
    except:
        wb = openpyxl.Workbook()
    sheet = wb['Sheet']
    sheet.cell(1,1).value ="m/k"
    sheet.cell(1,k+1).value =str(k)
    sheet.cell(m+1,1).value= str(m)
    j=1
    world = Population(1000,m,n,k)
 
    continuei = True
    if k>=n:
        j = n+1
    world.num_genes =j
    try:
        if sheet.cell(m+1, k+1).value < j-1:
        
            sheet.cell(m+1, k+1).value = str(j-1)
    except:
        sheet.cell(m+1, k+1).value = str(j-1)
        
    wb.save(filename)
    if old_world:
        old_world.k = k
        for indi in old_world.individuals:
            indi.k = k
        world = old_world
        j = old_world.num_genes
       
    while continuei:
        print("LET'SSSS GGOOOO")
        best = world.evolution(10000,mode, 0)        
        if best.fitness()[-1]:
            continuei =False
        else:
             
            world.bsort()
            new_world = Population(400,m,n,k,0)
            new_world.paths = world.paths
            new_world.l = world.l
            new_world.num_genes = j + 1
            j+=1
            if j-1 == len(new_world.paths):
                continuei = False
            try:
                if sheet.cell(m+1, k+1).value < j-1:
        
                    sheet.cell(m+1, k+1).value = str(j-1)
            except:
                sheet.cell(m+1, k+1).value = str(j-1)
            wb.save(filename)
            best.sequences.append(Sequence(m,n))
            new_world.individuals.append(best)
            new_world.best_fitness = best.fitness()[0]
            new_world.bfi = 0
            new_world.fitnesses.append(best.fitness()[0])#his fitness changed, so you have to recalculate it
            for i in range(1,int(0.1 * len(world.individuals))):
                world.individuals[i].sequences.append(Sequence(m,n))
                new_world.individuals.append(world.individuals[i])
                f=world.individuals[i].fitness()[0]
                if f > new_world.best_fitness:
                    new_world.best_fitness = f
                    
                new_world.fitnesses.append(f)
            assert len(new_world.individuals) == len(new_world.fitnesses)
            for a in range(len(new_world.fitnesses)):
                #print(new_world.individuals[a].fitness()[0],new_world.fitnesses[a])
                assert new_world.individuals[a].fitness()[0] == new_world.fitnesses[a]
            #assert False == True
                 
            world = new_world
    wb.close()
    return world
                
                
def collect_data(m,n):
    for i in range(m,12):
        world = run(i,n,3,"roulette") 
        for k in range(3+1,i+n):
            world=run(i,n,k,"roulette", world)
    
    
def wdw(m,n):
    paths = []
    #you can use while loop to make sure all paths are created
    for i in range(100000):
        l = Sequence(m,n)
        if l.terms not in paths:
            paths.append(l.terms)
    print(len(paths))
    return paths

def swdw(m,n):
    paths = []
    for i in range(10000):
        l = Sequence(m,n)
        if l.terms not in paths:
            paths.append(l.terms)
    #assert len(paths) == 56
    solutions = []      
    for i in range(len(paths)):
        a = Sequence(m,n,True)
        a.terms = paths[i]
        """
        p = test(9,5,3,4,"roulette",0)
        for j in range(56):
            l = Sequence(5,3)
            l.terms = paths[j]
            for seq in p.sequences:
                if seq.compare(l,4) == 0:
                    break
                elif seq == p.sequences[-1]:
                    while True:
                        print("FOUND!!!")
                        break
 
        """
if __name__ == "__main__":
    m = int(argv[1])
    collect_data(m,3)
