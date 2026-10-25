#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"values" = [dynamic]any{1, 2147483648},
}
_ = my_data
}
