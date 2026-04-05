#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"key" = "it's here",  // a comment
}
_ = my_data
}
