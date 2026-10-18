#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"within_i32" = 1705320000,
	"beyond_i32" = 4085195400,
}
_ = my_data
}
