#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"text" = "Record0(",
	"number" = 0x1,
}
_ = my_data
}
