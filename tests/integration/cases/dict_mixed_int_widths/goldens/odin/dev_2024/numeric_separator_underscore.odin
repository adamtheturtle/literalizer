#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"a" = 1,
	"b" = 3_000_000_000,
	"c" = "x",
}
_ = my_data
}
