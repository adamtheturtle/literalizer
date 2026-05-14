#+feature dynamic-literals
package main

main :: proc() {
val_x := map[string]any{
	"_" = "_",
}
val_y := map[string]any{
	"_" = "_",
}
my_data := [dynamic]any{
	val_x,
	val_y,
}
_ = my_data
}
