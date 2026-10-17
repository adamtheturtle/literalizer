#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"" = "unnamed",
	"named" = "value",
}
_ = my_data
}
