#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	")json" = "x",
}
_ = my_data
}
