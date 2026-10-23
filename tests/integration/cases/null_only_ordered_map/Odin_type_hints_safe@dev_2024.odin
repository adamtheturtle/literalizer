#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"missing" = nil,
}
_ = my_data
}
