#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"key" = "value \" # not a comment",  // real
}
_ = my_data
}
