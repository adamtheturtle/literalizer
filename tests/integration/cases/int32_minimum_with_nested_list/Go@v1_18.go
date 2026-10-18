package main

func main() {
my_data := map[string]any{
	"minimum": -2147483648,
	"neighbor": -2147483647,
	"maximum": 2147483647,
	"nested": []int{-2147483648},
}
_ = my_data
}
