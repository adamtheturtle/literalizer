#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"mixed" = [dynamic]any{[dynamic]any{"09:30:00"}, [dynamic]any{}},
}
_ = my_data
}
