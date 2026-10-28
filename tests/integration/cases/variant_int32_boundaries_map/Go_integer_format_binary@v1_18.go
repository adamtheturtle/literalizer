package main

func main() {
my_data := map[string]any{
	"below": -0b10000000000000000000000000000001,
	"minimum": -0b10000000000000000000000000000000,
	"above": -0b1111111111111111111111111111111,
	"nested": []int{0b0},
}
_ = my_data
}
