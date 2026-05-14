package main

func main() {
var my_data = map[int]struct{}{
	1: struct{}{},
	2: struct{}{},
	3: struct{}{},
}
my_data = map[int]struct{}{
	1: struct{}{},
	2: struct{}{},
	3: struct{}{},
}
_ = my_data
}
