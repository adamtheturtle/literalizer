#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"x" = "before\x00after",
}
_ = my_data
}
