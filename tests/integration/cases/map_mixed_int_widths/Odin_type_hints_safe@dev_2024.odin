#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"a" = 1,
	"b" = 1099511627776,
}
_ = my_data
}
