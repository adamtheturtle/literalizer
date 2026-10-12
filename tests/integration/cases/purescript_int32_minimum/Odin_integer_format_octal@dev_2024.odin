#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"minimum" = -0o20000000000,
	"neighbor" = -0o17777777777,
	"maximum" = 0o17777777777,
	"nested" = [dynamic]any{-0o20000000000},
}
_ = my_data
}
