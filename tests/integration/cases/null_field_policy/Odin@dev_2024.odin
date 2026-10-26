#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"drop" = nil,
	"keep" = 1,
}
_ = my_data
}
