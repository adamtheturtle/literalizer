#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"x" = "\x00",
	"y" = "\x001",
}
_ = my_data
}
