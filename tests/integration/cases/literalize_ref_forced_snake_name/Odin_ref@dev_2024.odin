#+feature dynamic-literals
package main

main :: proc() {
user_obj := map[string]any{
	"_" = "_",
}
my_data := user_obj
_ = my_data
}
