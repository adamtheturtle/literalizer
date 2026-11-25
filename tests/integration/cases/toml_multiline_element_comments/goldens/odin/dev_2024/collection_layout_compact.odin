#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"first" = [dynamic]any{1, 2},
	"second" = 3,  // About the second key.
}
_ = my_data
}
