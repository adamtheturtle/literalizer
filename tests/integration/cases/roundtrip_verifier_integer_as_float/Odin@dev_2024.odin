#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"value" = 1.0,
}
_ = my_data
}
