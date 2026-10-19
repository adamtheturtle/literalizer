#+feature dynamic-literals
package main
Record0 :: struct { name: string, payload: map[string]any }

main :: proc() {
my_data := [dynamic]any{
	Record0{ name = "one", payload = map[string]any{"scalar" = 1, "items" = [dynamic]any{}} },
	Record0{ name = "two", payload = map[string]any{"other" = 2} },
}
_ = my_data
}
