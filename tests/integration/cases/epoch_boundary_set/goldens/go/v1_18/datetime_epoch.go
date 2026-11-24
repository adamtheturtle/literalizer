package main

func main() {
my_data := map[int]struct{}{
	-2147483649: struct{}{},
	-2147483648: struct{}{},
	2147483647: struct{}{},
	2147483648: struct{}{},
}
_ = my_data
}
