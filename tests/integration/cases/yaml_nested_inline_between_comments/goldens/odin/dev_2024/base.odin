#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	[dynamic]any{2, "hello"},  // trailing note
	// next element
	[dynamic]any{3, "world"},
}
_ = my_data
}
