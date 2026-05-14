#+feature dynamic-literals
package main

main :: proc() {
my_var := map[string]any{
	"_" = "_",
}
my_data := my_var
_ = my_data
}
