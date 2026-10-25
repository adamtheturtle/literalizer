package main

func main() {
		Shared := []int{
			1,
			2,
		}
		my_data := []any{
			// A leading comment with { braces, "quotes", and // markers
			"first\n{ \"quoted\" // text }",
			Shared,
		}
_ = my_data
}
