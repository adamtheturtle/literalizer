#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"minimum" = -0x80000000,
	"below" = -0xb2d05e00,
}
_ = my_data
}
