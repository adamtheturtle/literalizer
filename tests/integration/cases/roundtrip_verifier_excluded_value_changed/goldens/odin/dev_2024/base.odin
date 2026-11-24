#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"keep" = true,
	"skip" = false,
}
_ = my_data
}
