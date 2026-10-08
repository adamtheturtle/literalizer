#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"not-a-field" = 1,
}
_ = my_data
}
