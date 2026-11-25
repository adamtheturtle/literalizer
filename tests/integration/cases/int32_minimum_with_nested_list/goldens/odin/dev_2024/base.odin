#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"minimum" = -2147483648,
	"neighbor" = -2147483647,
	"maximum" = 2147483647,
	"nested" = [dynamic]any{-2147483648},
}
_ = my_data
}
