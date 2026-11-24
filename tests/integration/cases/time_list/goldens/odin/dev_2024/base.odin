#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"times" = [dynamic]any{"09:30:00", "17:45:00", "23:59:59"},
}
_ = my_data
}
