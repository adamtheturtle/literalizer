#+feature dynamic-literals
package main

main :: proc() {
deep := map[string]any{
	"_" = "_",
}
my_data := map[string]any{
	"a" = map[string]any{"b" = map[string]any{"c" = deep}},
}
_ = my_data
}
