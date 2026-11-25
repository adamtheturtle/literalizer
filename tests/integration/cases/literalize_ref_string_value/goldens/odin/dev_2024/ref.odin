#+feature dynamic-literals
package main

main :: proc() {
shared := "s"
my_data := map[string]any{
	"value" = shared,
}
_ = my_data
}
