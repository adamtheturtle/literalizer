#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"minimum" = -0x80000000,
	"neighbor" = -0x7fffffff,
	"maximum" = 0x7fffffff,
	"nested" = [dynamic]any{-0x80000000},
}
_ = my_data
}
