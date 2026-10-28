package main

func main() {
var Shared = []int{
	1,
	2,
}
var Second = []int{
	3,
	4,
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
