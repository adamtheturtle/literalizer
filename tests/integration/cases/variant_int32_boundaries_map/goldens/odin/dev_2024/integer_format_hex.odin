#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"below" = -0x80000001,
	"minimum" = -0x80000000,
	"above" = -0x7fffffff,
	"nested" = [dynamic]any{0x0},
}
_ = my_data
}
