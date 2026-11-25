package main

func main() {
my_data := map[int64]struct{}{
	0o1: struct{}{},
	0o20000000000000: struct{}{},
}
_ = my_data
}
