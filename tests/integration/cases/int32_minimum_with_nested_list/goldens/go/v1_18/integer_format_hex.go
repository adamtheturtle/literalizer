package main

func main() {
my_data := map[string]any{
	"minimum": -0x80000000,
	"neighbor": -0x7fffffff,
	"maximum": 0x7fffffff,
	"nested": []int{-0x80000000},
}
_ = my_data
}
