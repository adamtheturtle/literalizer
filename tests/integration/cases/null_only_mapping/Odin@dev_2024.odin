#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"value" = nil,
}
_ = my_data
}
