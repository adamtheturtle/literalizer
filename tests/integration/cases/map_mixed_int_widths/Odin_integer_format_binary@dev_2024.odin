#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"a" = 0b1,
	"b" = 0b10000000000000000000000000000000000000000,
}
_ = my_data
}
