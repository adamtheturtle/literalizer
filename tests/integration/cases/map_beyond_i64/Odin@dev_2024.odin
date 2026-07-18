#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"a" = 9223372036854775807,
	"b" = 9223372036854775808,
}
_ = my_data
}
