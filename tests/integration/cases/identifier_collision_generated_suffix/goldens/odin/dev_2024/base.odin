#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"a-b" = 1,
	"a b" = 2,
	"a-b-2" = 3,
}
_ = my_data
}
