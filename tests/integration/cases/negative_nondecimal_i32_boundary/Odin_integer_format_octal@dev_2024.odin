#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"minimum" = -0o20000000000,
	"below" = -0o26264057000,
}
_ = my_data
}
