#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"minimum" = -0b10000000000000000000000000000000,
	"below" = -0b10110010110100000101111000000000,
}
_ = my_data
}
