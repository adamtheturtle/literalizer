#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	"prefix ${HOME} suffix",
	"${interpolated}",
}
_ = my_data
}
