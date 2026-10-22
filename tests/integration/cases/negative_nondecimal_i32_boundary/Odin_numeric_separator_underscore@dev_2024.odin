#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"minimum" = -2_147_483_648,
	"below" = -3_000_000_000,
}
_ = my_data
}
