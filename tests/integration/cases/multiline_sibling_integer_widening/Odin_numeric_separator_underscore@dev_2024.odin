#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"a" = [dynamic]any{1},
	"b" = [dynamic]any{1_099_511_627_776},
}
_ = my_data
}
