#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	// heading
	"count" = 2,
}
_ = my_data
}
