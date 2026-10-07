#+feature dynamic-literals
package main

main :: proc() {
bound := 2
my_data := map[string]any{
	"value" = bound,
}
_ = my_data
}
