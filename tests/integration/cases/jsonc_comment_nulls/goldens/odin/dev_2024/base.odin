#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	// null heading
	// before null
	"a" = nil,  // first null
	"b" = nil,  // second null
}
_ = my_data
}
