package main

func main() {
var Shared = []int{}
var Second = []int{
	1,
	2,
}
var my_data = [][]int{
	Shared,
	Second,
}
my_data = [][]int{
	Shared,
	Second,
}
_ = my_data
}
