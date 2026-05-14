#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"a" = nil,
	"b" = nil,
	// trailing
}
_ = my_data
}
