#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	"100% done",
	"%(name) is here",
}
_ = my_data
}
