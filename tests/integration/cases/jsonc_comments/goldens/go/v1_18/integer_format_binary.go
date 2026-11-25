package main

func main() {
my_data := map[string]any{
	// A JSONC input case with both comment forms.
	"url": "https://example.org/a/*b*/",  // detail
	// continued
	"count": 0b10,  // trailing line comment
}
_ = my_data
}
