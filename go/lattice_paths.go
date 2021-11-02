package main

import (
  "bufio"
  "os"
  "strings"
  "strconv"
)

const NUM_ATTR int = 8

type ComparisonData struct {
  // a struct for storing the information we would need about the k-distinctness of a particular m n k lattice
  // if struct attributes are updated, also update GenerateData function
  m int
  n int
  k int
  greedy_order int
  max_order int
  greedy_is_max bool
  greedy_set [][]bool
  max_sets [][][]bool
}

func fact_recursive(x int) int {
  // straightforward recursive factorial implementation
  if x == 1 {return 1}
  return x*fact(x-1)
}

func fact(x int) int {
  // straightforward nonrecursive factorial implementation
  res := 1
  for i := x; i > 1; i-- {
    res = res * i
  }
  return res
}

func comb(n, r int) int {
  // straightforward n choose r implementation
  if n==0 && r!=0 {return 0}
  return fact(n)/(fact(r)*fact(n-r))
}

func LexOrder(m, n int) [][]bool {
  // genereate all paths on the m by n lattice in lexicographic order
  path_num := comb(m+n,m) // number of unique paths
  paths := make([][]bool, path_num, path_num) // slice for storing paths
  paths[0] = make([]bool, m+n, m+n) // make the first path
  for i := m; i < m+n; i++ {
    paths[0][i] = true // set the last n valus to true (for north)
  }
  for i := 1; i < path_num; i++ {
    e_locs := make([]int, m, m) // slice for storing location of east steps
    e_counter := 0 // number of east steps encountered
    n_counter := 0 // number of north steps encountered
    var swap int // index of east step on which we will swap
    for j := 0; j < m+n; j++ {
      if paths[i-1][j] { // if it is a north step
        n_counter += 1 // incremement north steps
        if n_counter == n { // if we have encountered all north steps
          swap = e_locs[e_counter-1] // then, the swap is the most recent east step encountered
          break
        }
      } else { // if it is an east step
        e_locs[e_counter] = j // record east step location
        e_counter += 1 // increment east steps
        if e_counter == m { // if we have encountered all east steps
          swap = j // then, the current east step is the swap
          break
        }
      }
    }
    next_path := make([]bool, m+n, m+n)
    copy(next_path,paths[i-1]) // make a copy of the previous path lexicographically
    next_path[swap] = true // set swap east to be north
    next_path[swap+1] = false // set following north to be east
    for j := swap+2; j<m+n; j++ { // reverse the locations after
      next_path[j] = paths[i-1][m+n-(1+j-(swap+2))]
    }
    paths[i] = next_path // add the path to the paths
  }
  return paths
}

func LexOrderProcess(m, n int, ch chan []bool) {
  // generate all paths on the m by n lattice in lexicographic order and return them over a channel
  defer close(ch)
  path_num := comb(m+n,m) // number of unique paths
  prev_path := make([]bool, m+n, m+n) // make the first path
  for i := m; i < m+n; i++ {
    prev_path[i] = true // set the last n valus to true (for north)
  }
  ch <- prev_path // send the first path
  for i := 1; i < path_num; i++ {
    e_locs := make([]int, m, m) // slice for storing location of east steps
    e_counter := 0 // number of east steps encountered
    n_counter := 0 // number of north steps encountered
    var swap int // index of east step on which we will swap
    for j := 0; j < m+n; j++ {
      if prev_path[j] { // if it is a north step
        n_counter += 1 // incremement north steps
        if n_counter == n { // if we have encountered all north steps
          swap = e_locs[e_counter-1] // then, the swap is the most recent east step encountered
          break
        }
      } else { // if it is an east step
        e_locs[e_counter] = j // record east step location
        e_counter += 1 // increment east steps
        if e_counter == m { // if we have encountered all east steps
          swap = j // then, the current east step is the swap
          break
        }
      }
    }
    next_path := make([]bool, m+n, m+n)
    copy(next_path,prev_path) // make a copy of the previous path lexicographically
    next_path[swap] = true // set swap east to be north
    next_path[swap+1] = false // set following north to be east
    for j := swap+2; j<m+n; j++ { // reverse the locations after
      next_path[j] = prev_path[m+n-(1+j-(swap+2))]
    }
    ch <- next_path // send the next path
    prev_path = next_path
  }
}

func KDistinct(k int, path1, path2 []bool) bool {
  // test if two paths are k distinct
  if k==0 {return false} // if k is zero, no paths will be k distinct
  size := len(path1) // get length of paths we are comparing
  path1north := 0 // track the number of north steps in path 1
  path2north := 0 // track the number of north steps in path 2
  num_shared := 0 // track the number of shared edges
  for i := 0; i < size; i++ { // iterate over the paths
    if path1[i]==path2[i] && path1north==path2north { // if the paths take the same step and have the same number of north steps previously, they share an edge at i
      num_shared++ // increment the number of edges shared
      if num_shared == k { // if the paths share k edges, return false because they are not k distinct
        return false
      }
    }
    if path1[i] {path1north++} // if path 1 steps north, increment its north steps
    if path2[i] {path2north++} // if path 2 steps north, increment its north steps
  }
  return true // if we finish the loop without returning false, then the paths are k distinct and we return true
}

func KDistinctInSet(k int, path []bool, path_set [][]bool) bool {
  // test if a path is k distinct to all the paths in a given set of paths
  for _, x := range path_set { // we loop over the sets in the path set
    if !(KDistinct(k, path, x)) {return false} // if the path we are comparing is not k distinct with the current path from the set, return false
  }
  return true // if we reach the end of the loop without returning false, path is k distinct from all sets in the path set, and we return true
}

func SetKDistinct(k int, path_set [][]bool) bool {
  // test if all the paths within a set are k distinct
  equiv := false // assume the paths are k distinct
  for i := 0; i < len(path_set)-1; i++ { // iterate over all paths in the set
    if !(KDistinctInSet(k, path_set[i], path_set[i+1:])) { // see if the current path is k distinct from all following sets
      equiv = true // if not, we know we have a k-equivalence and we set that true and stop the loop
      break
    }
  }
  // if we reach the end of the loop without and equivalent sets, then equiv will be false
  return !(equiv) // return the opposite of the "contains equivalent sets" variable
}

func GreedyWithRoutine(m, n, k int) [][]bool {
  // implementation of the greedy algorithm for choosing a set of lattice paths
  path_set := make([][]bool, 0) // create a slice to store the paths
  channel := make(chan []bool, comb(m+n,m)) // create a channel to receive the paths
  go LexOrderProcess(m, n, channel) // start a process to generate the paths
  for x := range channel { // iterate over the paths
    if KDistinctInSet(k, x, path_set) { // if the path is distinct from all current paths
      path_set = append(path_set, x) // add it to the set
    }
  }
  return path_set // return the completed set of paths
}

func Greedy(m, n, k int) [][]bool {
  // implementation of the greedy algorithm for choosing a set of lattice paths
  path_set := make([][]bool, 0) // create a slice to store the paths
  for _, x := range LexOrder(m, n) { // loop over all paths in lexicographic order
    if KDistinctInSet(k, x, path_set) { // if the path is distinct from all current paths
      path_set = append(path_set, x) // add it to the set
    }
  }
  return path_set // return the completed set of paths
}

func UpperBound(m, n, k int) int {
  // a function to generate an upper bound for a maximum set of k distinct lattice paths
  // the current upper bound counts the number of distinct ways to starts to a path on the m by n lattice, with a start being of length k
  up_bound := 0 // counter for the combinations sum
  var start int = 0 // if k is less than m, we start at choosing zero
  if k-m > 0 { // otherwise, we start at k minus m
    start = k-m
  }
  for i := start; i <= n; i++ {
    up_bound += comb(k,i) // sum all k choose i for i between our start value and n
  }
  return up_bound // return the upper bound
}

func CombinationsProcess(m, n, size int, ch chan [][]bool) {
  // a function that generates all combinations of paths on a given lattice in sets of a given size, and sends them to a channel
  defer close(ch)
  num := comb(m+n, m) // the number of paths
  if size > num {return} // we can't form a set with more paths than we have
  paths := LexOrder(m,n) // get the paths
  indices := make([]int, size) // create a slice that will hold the indices for the paths we are currently considering
  for i := 0; i < size; i++ {
    indices[i] = i // initialize the indices to 0, 1, 2, ... , size-1
  }
  next_set := make([][]bool, size) // creating a slice to hold the current set
  for i, x := range indices {
    next_set[i] = paths[x] // initialize the current set to paths number 0, 1, 2, ..., size-1
  }
  ch <- next_set // send the current set
  var not_last bool = true // track whether we have the last set
  for not_last {
    not_last = false // assume we have the last set
    for i := size-1; i >= 0; i-- { // loop backwards through the indices
      if indices[i] != num-(size-i) { // if the given index does not equal the maximum value for that index, we have another set
        indices[i]+=1 // increment the index that is not at the max
        for j := i+1; j<size; j++ { // for all following indices
          indices[j] = indices[i]+(j-i) // the index should be equal to the currently incremented index plus the number of steps away from that index it is
        }
        for k, x := range indices {
          next_set[k] = paths[x] // update the next set with the paths from the given indices
        }
        ch <- next_set // send the next path to the channel
        not_last = true // if we've created another path, we could have another one
        break
      }
    }
  }
}

func FindDistinctSets(m, n, k, size int, ch chan [][]bool) {
  // a functiont to find all k distinct sets of a given size
  defer close(ch)
  in_chan := make(chan [][]bool) // create a channel to receive combinations
  go CombinationsProcess(m,n,size,in_chan) // start a process to send combinations
  for set := range in_chan { // for all the sets of paths
    if SetKDistinct(k, set) { // if it is k distinct, send it to the channel
      ch <- set
    }
  }
}

func CombinationsAndDistinct(m, n, k, size int) [][][]bool {
  // a function to generate all possible combinations and check them for distinctness simultaneously
  // I created this function to try to reduce the number of goroutines created while generating data because I was overflowing the goroutine stack
  num := comb(m+n, m) // the number of paths
  if size > num {return nil} // we can't form a set with more paths than we have
  distinct_combos := make([][][]bool,0) // a slice to hold all the distinct combinations that we find
  paths := LexOrder(m,n) // get the paths
  indices := make([]int, size) // create a slice that will hold the indices for the paths we are currently considering
  for i := 0; i < size; i++ {
    indices[i] = i // initialize the indices to 0, 1, 2, ... , size-1
  }
  next_set := make([][]bool, size) // creating a slice to hold the current set
  for i, x := range indices {
    next_set[i] = paths[x] // initialize the current set to paths number 0, 1, 2, ..., size-1
  }
  if SetKDistinct(k, next_set) { // if the first set is k distinct
    distinct_combos = append(distinct_combos, next_set) // add it to the set of k distinct sets
  }
  var not_last bool = true // track whether we have the last set
  for not_last {
    not_last = false // assume we have the last set
    for i := size-1; i >= 0; i-- { // loop backwards through the indices
      if indices[i] != num-(size-i) { // if the given index does not equal the maximum value for that index, we have another set
        indices[i]+=1 // increment the index that is not at the max
        for j := i+1; j<size; j++ { // for all following indices
          indices[j] = indices[i]+(j-i) // the index should be equal to the currently incremented index plus the number of steps away from that index it is
        }
        for k, x := range indices {
          next_set[k] = paths[x] // update the next set with the paths from the given indices
        }
        if SetKDistinct(k, next_set) { // if the set is k distinct
          distinct_combos = append(distinct_combos, next_set) // add it to the set of k distinct sets
        }
        not_last = true // if we've created another path, we could have another one
        break
      }
    }
  }
  if len(distinct_combos)==0 { // if there are no distinct sets
    return nil // return nil
  }
  return distinct_combos // return the set of distinct sets
}

func GreedyMaxComparisonMoreRoutines(m, n, k int, ch chan ComparisonData) {
  // a function to compare the results given by the greedy algorthim to a brute force search
  // this is the initial function I wrote for generating data, and it kept crashing because of a goroutine stack overflow
  result := ComparisonData{m: m, n: n, k: k} // store m, n, and k
  result.greedy_set = Greedy(m,n,k) // get the greedy set for the given m, n, and k
  result.greedy_order = len(result.greedy_set) // store the cardinality of the greedy set
  up_bound := UpperBound(m, n, k) // get the upper bound for the current lattice size and k
  if up_bound == result.greedy_order { // if the greedy cardinality is at the upper bound, we know it returns maximum
    result.greedy_is_max = true // then, the greedy is maximum
    result.max_order = up_bound // the max order is the upper bound ( same as greedy order )
    max_sets := make([][][]bool, 0) // create a slice to store all maximum sets
    channel := make(chan [][]bool) // create a channel to get the sets
    go FindDistinctSets(m,n,k,up_bound, channel) // start a process to find all the distinct maximum sets
    for set := range channel {
      max_sets = append(max_sets,set) // store the sets
    }
    result.max_sets = max_sets // update the struct
  } else { // if the greedy set cardinality is not the upper bound, we need to consider other sizes of set
    size := up_bound // start checking the sets at the upper bound
    max_sets := make([][][]bool, 0) // create a slice to store the potentially maximum sets
    for len(max_sets)==0 { // as long as the length of the max_sets slice is zero, we need to look for a smaller size of set
      channel := make(chan [][]bool) // create a channel to receive the sets
      go FindDistinctSets(m,n,k,size, channel) // start a process to find all the distinct sets of the current size
      for set := range channel {
        max_sets = append(max_sets,set) // store the sets
      }
      size-- // decrement the size variable, in case we need to keep looking
    }
    size++ // once we have a nonzero set of sets, we know that we just decremented size, so we increment it to get the size we actually used
    result.max_order = size // the maxmimum order is given by the size we just used
    result.max_sets = max_sets // the maximum sets are given by the sets we just found
    result.greedy_is_max = result.max_order == result.greedy_order // the greedy algorithm is maximum if the maximum order equals the greedy order
  }
  ch <- result // return the struct
}

func GreedyMaxComparison(m, n, k int, ch chan ComparisonData) {
  // a function to compare the results given by the greedy algorthim to a brute force search
  result := ComparisonData{m: m, n: n, k: k} // store m, n, and k
  result.greedy_set = Greedy(m,n,k) // get the greedy set for the given m, n, and k
  result.greedy_order = len(result.greedy_set) // store the cardinality of the greedy set
  up_bound := UpperBound(m, n, k) // get the upper bound for the current lattice size and k
  if up_bound == result.greedy_order { // if the greedy cardinality is at the upper bound, we know it returns maximum
    result.greedy_is_max = true // then, the greedy is maximum
    result.max_order = up_bound // the max order is the upper bound ( same as greedy order )
    result.max_sets = CombinationsAndDistinct(m, n, k, up_bound) // generate and store all maximum sets
  } else { // if the greedy set cardinality is not the upper bound, we need to consider other sizes of set
    size := up_bound + 1 // start checking the sets at the upper bound; we add 1 initially because we always decrement the size
    var max_sets [][][]bool // create a slice to store the potentially maximum sets
    for max_sets==nil { // as long as the max sets slice contains no sets, we need to look for a smaller size of set
      size-- // decrement the size variable to find sets of the next possible size
      max_sets = CombinationsAndDistinct(m, n, k, size) // generate and store all sets of the size we are curerntly considering
    }
    result.max_order = size // the maxmimum order is the size we have when finally find some maximum sets
    result.max_sets = max_sets // the sets are the current set of maximum sets
    result.greedy_is_max = result.max_order == result.greedy_order // the greedy algorithm is maximum if the maximum order equals the greedy order
  }
  ch <- result // return the struct
}

func GenerateData(m, n int, outfile_name string) {
  // a function for generating data comparing the greedy algorithm to a brute force search on a particular size of lattice
  channel := make(chan ComparisonData, m+n) // create a channel for receiving data
  defer close(channel) // close the channel when we finish
  for k := 0; k <= m+n; k++ { // for all sizes of k, start a routine to generate the needed data
    go GreedyMaxComparison(m, n, k, channel)
  }
  file, _ := os.OpenFile(outfile_name, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644) // open a file for storing the output
  defer file.Close() // close the file when we finish
  datawriter := bufio.NewWriter(file) // create a writer to write to the file
  defer datawriter.Flush() // flush the writer when we finish
  var next_row ComparisonData // create a variable to store the next row we receive from the routines
  var next_row_strings [NUM_ATTR]string // there will be the same number of variables to store as attributes that we have
  for k := 0; k <= m+n; k++ { // for each k value
    next_row = <-channel // get the next row from the buffered channel
    next_row_strings[0] = strconv.Itoa(next_row.m) // convert m to a string
    next_row_strings[1] = strconv.Itoa(next_row.n) // convert n to a string
    next_row_strings[2] = strconv.Itoa(next_row.k) // convert k to a string
    next_row_strings[3] = strconv.Itoa(next_row.greedy_order) // convert the greedy order to a string
    next_row_strings[4] = strconv.Itoa(next_row.max_order) // convert the maximum order to a string
    next_row_strings[5] = strconv.FormatBool(next_row.greedy_is_max) // conver the greedy is max? boolean to a string
    greedy_set := "[" // create a string for storing the greedy set in string form
    for i, x := range next_row.greedy_set { // for each path in the greedy set
      next_path := "" // create a string for storing the path in string form
      for _, y := range x { // for each step in the path, convert it to a character for easy reading and reviewing
        if y {
          next_path = next_path + "N"
        } else {
          next_path = next_path + "E"
        }
      }
      greedy_set = greedy_set + next_path // append the next path string to our greedy set string
      if i != next_row.greedy_order - 1 { // if we haven't gotten to the last path yet, add a comma
        greedy_set = greedy_set + ", "
      }
    }
    greedy_set = greedy_set + "]" // close the string
    next_row_strings[6] = greedy_set // update the list of strings with the string for the greedy set
    max_sets := "[" // create a string for storing the set of maximum sets in string form
    for i, x := range next_row.max_sets { // for each set of paths in the set of maximum sets
      next_set := "[" // create a string for storing the set in string form
      for j, y := range x { // for each path in the current set
        next_path := "" // create a string for storing the path in string form
        for _, z := range y { // for each step in the path, conver it to a character
          if z {
            next_path = next_path + "N"
          } else {
            next_path = next_path + "E"
          }
        }
        next_set = next_set + next_path // add the path to the current set of paths in string form
        if j != next_row.max_order - 1 { // if this is not the last path in the set, add a comma
          next_set = next_set + ", "
        }
      }
      next_set = next_set + "]"
      max_sets = max_sets + next_set // add the current set to the list of maximum sets
      if i != len(next_row.max_sets)-1 { // if this is not the last maxmimum path set, add a comma
        max_sets = max_sets + ", "
      }
    }
    max_sets = max_sets + "]"
    next_row_strings[7] = max_sets // add the string of maximum sets of paths to the string array
    next_row_out := strings.Join(next_row_strings[:], "\t") // the next row is a tab separated string of the each element in the array of ouput strings
    datawriter.WriteString(next_row_out + "\n") // write the next row to the output
    datawriter.Flush() // flush the datawriter so it writes the row to the file
  }
}

func main() {
  args := os.Args[1:] // get the command line arguments
  m, _ := strconv.Atoi(args[0]) // the first argument should be m
  n, _ := strconv.Atoi(args[1]) // the second argument should be n
  GenerateData(m,n,args[2]) // generate the data for the m by n lattice, the last command line argument should be the output file name
}
