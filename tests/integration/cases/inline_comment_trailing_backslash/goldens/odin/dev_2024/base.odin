#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"a" = 1,  // inline ending backslash \ .
	"b" = 2,
}
_ = my_data
}
