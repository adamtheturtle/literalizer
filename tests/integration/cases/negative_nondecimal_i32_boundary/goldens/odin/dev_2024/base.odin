#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"minimum" = -2147483648,
	"below" = -3000000000,
}
_ = my_data
}
