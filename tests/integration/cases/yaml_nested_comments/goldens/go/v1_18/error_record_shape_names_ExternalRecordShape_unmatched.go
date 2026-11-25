package main

func main() {
my_data := map[string]any{
	"a": map[string]int{
		// inner note
		"b": 1,  // inline b
	},
	"list": []int{
		1,  // first
		2,  // second
	},
}
_ = my_data
}
