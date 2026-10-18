#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"b" = map[string]any{"k" = 1},
	"a" = map[string]any{"k" = 2208988800},
}
_ = my_data
}
