#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"quantity" = 1000000,
	"big" = 18446744073709551615,
	"ratio" = 2.5,
	"label" = "tag",
	"ok" = true,
}
_ = my_data
}
