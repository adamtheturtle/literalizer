package main

func main() {
my_data := map[string]any{
	"flow": []int{
		1,
		// After the first element.
		2,
	},
	// Between the key and its value.
	"gap": 3,
	// On the block scalar header.
	"block": "Text.\n",
	"nested": []int{
		1,
		1,
		// On the nested alias.
	},
	"anchored": 4,
	"alias": 4,
	// On the alias.
}
_ = my_data
}
