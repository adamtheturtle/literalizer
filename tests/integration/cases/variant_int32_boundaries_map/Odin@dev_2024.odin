#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"below" = -2147483649,
	"minimum" = -2147483648,
	"above" = -2147483647,
	"nested" = [dynamic]any{0},
}
_ = my_data
}
