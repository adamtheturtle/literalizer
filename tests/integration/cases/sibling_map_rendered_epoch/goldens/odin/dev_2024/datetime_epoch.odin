#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"a" = map[string]any{"k" = 2208988800},
	"b" = map[string]any{"k" = 1},
}
_ = my_data
}
