package main

func main() {
my_data := map[string]any{
	"below": -0x80000001,
	"minimum": -0x80000000,
	"above": -0x7fffffff,
	"nested": []int{0x0},
}
_ = my_data
}
