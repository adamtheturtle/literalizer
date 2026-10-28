#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"below" = -0o20000000001,
	"minimum" = -0o20000000000,
	"above" = -0o17777777777,
	"nested" = [dynamic]any{0o0},
}
_ = my_data
}
