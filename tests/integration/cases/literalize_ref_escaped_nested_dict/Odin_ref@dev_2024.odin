#+feature dynamic-literals
package main

main :: proc() {
existing := 1
my_data := map[string]any{
	"nested" = [dynamic]any{0, existing},
}
_ = my_data
}
