package main

func main() {
Shared := []int{
	1,
	2,
}
my_data := []map[string][]int{
	{"left": Shared, "right": Shared},
}
_ = my_data
}
