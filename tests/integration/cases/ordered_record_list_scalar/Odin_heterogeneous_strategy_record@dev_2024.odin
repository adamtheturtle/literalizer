#+feature dynamic-literals
package main
Record0 :: struct { id: int }

main :: proc() {
my_data := map[string]any{
	"first" = [dynamic]any{Record0{ id = 1 }},
	"second" = 2,
}
_ = my_data
}
