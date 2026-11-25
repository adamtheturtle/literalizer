package main

func main() {
my_data := map[int64]struct{}{
	0x1: struct{}{},
	0x10000000000: struct{}{},
}
_ = my_data
}
