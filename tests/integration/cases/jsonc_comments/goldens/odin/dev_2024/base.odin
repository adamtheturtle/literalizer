#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	// A JSONC input case with both comment forms.
	"url" = "https://example.org/a/*b*/",  // detail
	// continued
	"count" = 2,  // trailing line comment
}
_ = my_data
}
