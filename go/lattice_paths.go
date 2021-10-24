package main

import (
  "bufio"
  "os"
  "strings"
  "strconv"
)

const NUM_ATTR int = 8

type ComparisonData struct {
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

func fact(x int) int {
  // straightforward recursive factorial implementation
  if x == 1 {return 1}
  return x*fact(x-1)
}

func comb(p, q int) int {
  return fact(p)/(fact(q)*fact(p-q))
}

func LexOrder(m, n int) [][]bool {
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
  size := len(path1)
  path1north := 0
  path2north := 0
  num_shared := 0
  for i := 0; i < size; i++ {
    if path1[i]==path2[i] && path1north==path2north {
      num_shared++
      if num_shared >= k {
        return false
      }
    }
    if path1[i] {path1north++}
    if path2[i] {path2north++}
  }
  return true
}

func KDistinctInSet(k int, path []bool, path_set [][]bool) bool {
  for _, x := range path_set {
    if !(KDistinct(k, path, x)) {return false}
  }
  return true
}

func SetKDistinct(k int, path_set [][]bool) bool {
  equiv := false
  for i := 0; i < len(path_set)-1; i++ {
    if !(KDistinctInSet(k, path_set[i], path_set[i+1:])) {
      equiv = true
      break
    }
  }
  return !(equiv)
}

func Greedy(m, n, k int) [][]bool {
  path_set := make([][]bool, 0)
  channel := make(chan []bool, comb(m+n,m))
  go LexOrderProcess(m, n, channel)
  for x := range channel {
    if KDistinctInSet(k, x, path_set) {
      path_set = append(path_set, x)
    }
  }
  return path_set
}

func UpperBound(m, n, k int) int {
  up_bound := 0
  var start int = 0
  if k-m > 0 {
    start = k-m
  }
  for i := start; i < n+1; i++ {
    up_bound += comb(k,i)
  }
  return up_bound
}

func CombinationsProcess(m, n, size int, ch chan [][]bool) {
  defer close(ch)
  num := comb(m+n, m)
  if size > num {return}
  paths := LexOrder(m,n)
  indices := make([]int, size)
  for i := 0; i < size; i++ {
    indices[i] = i
  }
  next_set := make([][]bool, size)
  for i, x := range indices {
    next_set[i] = paths[x]
  }
  ch <- next_set
  var not_last bool = true
  for not_last {
    not_last = false
    for i := size-1; i >= 0; i-- {
      if indices[i] != num-(size-i) {
        indices[i]+=1
        for j := i+1; j<size; j++ {
          indices[j] = indices[i]+(j-i)
        }
        for k, x := range indices {
          next_set[k] = paths[x]
        }
        ch <- next_set
        not_last = true
        break
      }
    }
  }
}

func FindDistinctSets(m, n, k, size int, ch chan [][]bool) {
  defer close(ch)
  in_chan := make(chan [][]bool)
  go CombinationsProcess(m,n,size,in_chan)
  for set := range in_chan {
    if SetKDistinct(k, set) {
      ch <- set
    }
  }
}

func GreedyMaxComparison(m, n, k int, ch chan ComparisonData) {
  result := ComparisonData{m: m, n: n, k: k}
  result.greedy_set = Greedy(m,n,k)
  result.greedy_order = len(result.greedy_set)
  up_bound := UpperBound(m, n, k)
  if up_bound == result.greedy_order {
    result.greedy_is_max = true
    result.max_order = up_bound
    max_sets := make([][][]bool, 0)
    channel := make(chan [][]bool)
    go FindDistinctSets(m,n,k,up_bound, channel)
    for set := range channel {
      max_sets = append(max_sets,set)
    }
    result.max_sets = max_sets
  } else {
    size := up_bound
    max_sets := make([][][]bool, 0)
    for len(max_sets)==0 {
      channel := make(chan [][]bool)
      go FindDistinctSets(m,n,k,size, channel)
      for set := range channel {
        max_sets = append(max_sets,set)
      }
      size--
    }
    size++
    result.max_order = size
    result.max_sets = max_sets
    result.greedy_is_max = result.max_order == result.greedy_order
  }
  ch <- result
}

func GenerateData(m, n int, outfile_name string) {
  channel := make(chan ComparisonData)
  defer close(channel)
  for k := 0; k <= m+n; k++ {
    go GreedyMaxComparison(m, n, k, channel)
  }
  file, err := os.OpenFile(outfile_name, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
  if err != nil {
    file, _ = os.Create(outfile_name)
  }
  defer file.Close()
  datawriter := bufio.NewWriter(file)
  defer datawriter.Flush()
  var next_row ComparisonData
  var next_row_strings [NUM_ATTR]string
  for k := 0; k <= m+n; k++ {
    next_row = <-channel
    next_row_strings[0] = strconv.Itoa(next_row.m)
    next_row_strings[1] = strconv.Itoa(next_row.n)
    next_row_strings[2] = strconv.Itoa(next_row.k)
    next_row_strings[3] = strconv.Itoa(next_row.greedy_order)
    next_row_strings[4] = strconv.Itoa(next_row.max_order)
    next_row_strings[5] = strconv.FormatBool(next_row.greedy_is_max)
    greedy_set := "["
    for i, x := range next_row.greedy_set {
      next_path := ""
      for _, y := range x {
        if y {
          next_path = next_path + "N"
        } else {
          next_path = next_path + "E"
        }
      }
      greedy_set = greedy_set + next_path
      if i != next_row.greedy_order - 1 {
        greedy_set = greedy_set + ", "
      }
    }
    greedy_set = greedy_set + "]"
    next_row_strings[6] = greedy_set
    max_sets := "["
    for i, x := range next_row.max_sets {
      next_set := "["
      for j, y := range x {
        next_path := ""
        for _, z := range y {
          if z {
            next_path = next_path + "N"
          } else {
            next_path = next_path + "E"
          }
        }
        next_set = next_set + next_path
        if j != next_row.max_order - 1 {
          next_set = next_set + ", "
        }
      }
      next_set = next_set + "]"
      max_sets = max_sets + next_set
      if i != len(next_row.max_sets)-1 {
        max_sets = max_sets + ", "
      }
    }
    max_sets = max_sets + "]"
    next_row_strings[7] = max_sets
    next_row_out := strings.Join(next_row_strings[:], "\t")
    datawriter.WriteString(next_row_out + "\n")
    datawriter.Flush()
  }
}

func main() {
  args := os.Args[1:]
  m, _ := strconv.Atoi(args[0])
  n, _ := strconv.Atoi(args[1])
  GenerateData(m,n,args[2])
}
