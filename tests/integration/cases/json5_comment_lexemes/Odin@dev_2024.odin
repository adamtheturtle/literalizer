#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	// heading
	"a" = "single ' // data",
	"b" = "linecontinuation",
	"c" = "\\",  // actual comment
	"d" = "  ",  // final comment
}
_ = my_data
}
