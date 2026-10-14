package main

func main() {
Shared := []int{}
Second := []int{
	1,
	2,
}
my_data := [][]int{
	Shared,
	Second,
}
my_data = [][]int{
	Shared,
	Second,
}
_ = my_data
}
