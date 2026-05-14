#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"vals" = [dynamic]any{"2024-01-15", "09:30:00"},
}
_ = my_data
}
