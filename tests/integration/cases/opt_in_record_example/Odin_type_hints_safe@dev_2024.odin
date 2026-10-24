#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"name" = "Ada",
	"active" = true,
	"scores" = [dynamic]any{1, 2, 3},
}
_ = my_data
}
