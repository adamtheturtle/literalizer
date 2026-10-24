#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"a" = 0o1,
	"b" = 2.5,
	"c" = 0o3,
}
_ = my_data
}
