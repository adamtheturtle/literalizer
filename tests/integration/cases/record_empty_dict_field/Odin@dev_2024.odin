#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"f" = map[string]any{},
	"g" = 1,
}
_ = my_data
}
