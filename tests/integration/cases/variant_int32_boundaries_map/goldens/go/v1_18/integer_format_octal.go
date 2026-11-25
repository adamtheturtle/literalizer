package main

func main() {
my_data := map[string]any{
	"below": -0o20000000001,
	"minimum": -0o20000000000,
	"above": -0o17777777777,
	"nested": []int{0o0},
}
_ = my_data
}
