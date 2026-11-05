#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"v" = "a\ufeffb",
}
_ = my_data
}
