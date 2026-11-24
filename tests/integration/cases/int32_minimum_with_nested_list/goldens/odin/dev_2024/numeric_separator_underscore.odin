#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"minimum" = -2_147_483_648,
	"neighbor" = -2_147_483_647,
	"maximum" = 2_147_483_647,
	"nested" = [dynamic]any{-2_147_483_648},
}
_ = my_data
}
