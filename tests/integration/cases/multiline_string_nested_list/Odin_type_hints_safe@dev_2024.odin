#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	[dynamic]any{"\nfirst line\n  indented\n\nlast line\n"},
}
_ = my_data
}
