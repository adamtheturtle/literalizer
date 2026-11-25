#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"a" = 0x1,
	"b" = 0x10000000000,
}
_ = my_data
}
