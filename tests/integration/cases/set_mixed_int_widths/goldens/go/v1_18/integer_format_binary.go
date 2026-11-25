package main

func main() {
my_data := map[int64]struct{}{
	0b1: struct{}{},
	0b10000000000000000000000000000000000000000: struct{}{},
}
_ = my_data
}
