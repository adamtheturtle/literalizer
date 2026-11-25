#+feature dynamic-literals
package main

main :: proc() {
userObj := map[string]any{
	"_" = "_",
}
my_data := userObj
_ = my_data
}
