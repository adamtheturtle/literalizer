#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"a-b" = 1,
	"a-b-2" = 2,
	"a b" = 3,
}
_ = my_data
}
