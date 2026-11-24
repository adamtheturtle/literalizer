package main

func main() {
var Shared = []int{
	1,
	2,
}
var Second = []string{
	"one",
	"two",
}
var my_data = []any{
	Shared,
	Second,
}
_ = my_data
}
