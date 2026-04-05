#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	"issue #{42}",
	"color #red",
}
_ = my_data
}
