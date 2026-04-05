#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	"line1\r\nline2",
	"line1\rline2",
	"",
}
_ = my_data
}
