package main

func main() {
my_data := map[string]any{
	"a": map[string]any{
		"b": []int{1},
		// Outdented from the sequence, so the inner mapping claims this.
		"c": 2,
	},
	// Outdented from the inner mapping too, so the root claims this.
	"d": 3,
}
_ = my_data
}
