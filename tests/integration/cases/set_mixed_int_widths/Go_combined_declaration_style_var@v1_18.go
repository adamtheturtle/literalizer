package main

func main() {
var my_data = map[int]struct{}{
	1: struct{}{},
	1099511627776: struct{}{},
}
my_data = map[int]struct{}{
	1: struct{}{},
	1099511627776: struct{}{},
}
_ = my_data
}
