#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	"2024-01-15",
	"2024-02-20",
}
_ = my_data
}
