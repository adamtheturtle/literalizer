#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"08" = "value",
}
_ = my_data
}
