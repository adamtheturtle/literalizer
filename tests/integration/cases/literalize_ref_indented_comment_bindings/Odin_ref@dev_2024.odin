#+feature dynamic-literals
package main

main :: proc() {
		shared := [dynamic]any{
			1,
			2,
		}
		my_data := [dynamic]any{
			// A leading comment with { braces, "quotes", and // markers
			"first\n{ \"quoted\" // text }",
			shared,
		}
_ = my_data
}
