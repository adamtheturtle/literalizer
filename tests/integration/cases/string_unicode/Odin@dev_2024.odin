#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	"café",
	"中文",
}
_ = my_data
}
