package main

func main() {
Shared := []int{
	1,
	2,
}
Second := []int{
	3,
	4,
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
