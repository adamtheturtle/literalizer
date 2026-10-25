#+feature dynamic-literals
package main

main :: proc() {
	shared := [dynamic]any{
		1,
		2,
	}
	my_data := map[string]any{
		"a" = shared,
	}
_ = my_data
}
