package main

func main() {
my_data := []any{
	[]any{
		map[string]string{"item": "existing"},
		"kept",
		// This comment trails the first pair.
	},
	[]any{map[string]string{"item": "next"}, "also kept"},
	// This comment describes the last pair.
	[]any{map[string]string{"item": "last"}, "kept too"},
}
my_data = []any{
	[]any{
		map[string]string{"item": "existing"},
		"kept",
		// This comment trails the first pair.
	},
	[]any{map[string]string{"item": "next"}, "also kept"},
	// This comment describes the last pair.
	[]any{map[string]string{"item": "last"}, "kept too"},
}
_ = my_data
}
