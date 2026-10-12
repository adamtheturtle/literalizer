#+feature dynamic-literals
package main

main :: proc() {
			shared := [dynamic]any{
				1,
				2,
			}
			other := 3
			payload := "\n    shared : Val\nshared = RInt 99"
			my_data := map[string]any{
				"a" = shared,
				"b" = other,
				"payload" = payload,
			}
_ = my_data
}
