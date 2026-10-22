#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"a" = 0o1,
	"b" = 0o20000000000000,
}
_ = my_data
}
