#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"minimum" = -0b10000000000000000000000000000000,
	"neighbor" = -0b1111111111111111111111111111111,
	"maximum" = 0b1111111111111111111111111111111,
	"nested" = [dynamic]any{-0b10000000000000000000000000000000},
}
_ = my_data
}
