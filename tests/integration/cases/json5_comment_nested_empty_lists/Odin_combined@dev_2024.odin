#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	// outer heading
	// first empty
	[dynamic]any{},
	// second empty
	[dynamic]any{},
}
my_data = [dynamic]any{
	// outer heading
	// first empty
	[dynamic]any{},
	// second empty
	[dynamic]any{},
}
_ = my_data
}
