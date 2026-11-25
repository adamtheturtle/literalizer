#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	// outer heading
	// first empty
	"a" = map[string]any{},
	// second empty
	"b" = map[string]any{},
}
my_data = map[string]any{
	// outer heading
	// first empty
	"a" = map[string]any{},
	// second empty
	"b" = map[string]any{},
}
_ = my_data
}
