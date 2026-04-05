#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"a" = 1,
	"b" = 2.5,
	"c" = 3,
}
_ = my_data
}
