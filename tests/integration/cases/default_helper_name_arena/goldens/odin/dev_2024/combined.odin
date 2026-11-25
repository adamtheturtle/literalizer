#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"a" = 1,
}
my_data = map[string]any{
	"a" = 1,
}
_ = my_data
}
