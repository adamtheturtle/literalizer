#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"a" = [dynamic]any{4294967296, 4294967297},
}
_ = my_data
}
