#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"keep" = true,
	"skip" = 0,
}
_ = my_data
}
