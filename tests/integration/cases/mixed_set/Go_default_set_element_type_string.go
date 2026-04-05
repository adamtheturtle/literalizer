package main

func main() {
my_data := map[string]struct{}{
	true: struct{}{},
	42: struct{}{},
	"apple": struct{}{},
}
_ = my_data
}
