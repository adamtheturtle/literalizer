package main

func main() {
		var Shared = []int{
			1,
			2,
		}
		var my_data = []any{
			// A leading comment with { braces, "quotes", and // markers
			"first\n{ \"quoted\" // text }",
			Shared,
		}
_ = my_data
}
