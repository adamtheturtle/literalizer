#+feature dynamic-literals
package main

main :: proc() {
existing := map[string]any{
	"_" = "_",
}
my_data := existing
_ = my_data
}
